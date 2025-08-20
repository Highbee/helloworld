import re
from datetime import datetime, timedelta

def parse_duration_to_minutes(duration_str):
    if not duration_str or not isinstance(duration_str, str) or duration_str.lower().strip() in ['nil', 'n/a', '']:
        return None

    duration_str = duration_str.lower().strip()
    total_minutes = 0

    try:
        hours_match = re.search(r'(\d+)\s*(?:hr|hour|hrs)', duration_str)
        if hours_match:
            total_minutes += int(hours_match.group(1)) * 60

        minutes_match = re.search(r'(\d+)\s*(?:min|mins|minutes|m)', duration_str)
        if minutes_match:
            total_minutes += int(minutes_match.group(1))

        if ':' in duration_str and not hours_match and not minutes_match:
            parts = duration_str.split(':')
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                total_minutes = int(parts[0]) * 60 + int(parts[1])

        if total_minutes == 0 and duration_str.isdigit():
             total_minutes = int(duration_str) * 60

    except (ValueError, IndexError):
        return None

    return total_minutes if total_minutes > 0 else None


def parse_time(time_str, date_obj, previous_datetime=None):
    if not time_str or not isinstance(time_str, str) or time_str.lower().strip() in ['nil', 'n/a', '', 'never reach keeping', 'no keep', 'no keeping time']:
        return None

    time_str = time_str.strip().upper()

    if '/' in time_str:
        parts = time_str.split('/')
        time_str = parts[0].strip()
        try:
            date_obj = datetime.strptime(parts[1].strip(), '%d-%m-%Y').date()
        except ValueError:
            pass

    time_str = re.sub(r'([AP]M).*', r'\1', time_str)

    dt = None
    for fmt in ('%I:%M%p', '%I:%M %p', '%H:%M', '%I%p', '%I %p', '%H.%M'):
        try:
            dt = datetime.strptime(f"{date_obj.strftime('%Y-%m-%d')} {time_str}", f'%Y-%m-%d {fmt}')
            break
        except ValueError:
            continue

    if not dt:
        return None

    if previous_datetime and dt.hour < previous_datetime.hour and not (previous_datetime.hour > 12 and dt.hour < 12):
         dt += timedelta(days=1)

    return dt

def parse_whatsapp_chat(chat_file):
    with open(chat_file, 'r', encoding='utf-8') as f:
        content = f.read()

    reports = {}

    pattern = re.compile(
        r"\[(\d{2}/\d{2}/\d{4}\s\d{2}:\d{2})\]\s([^:]+):\s([\s\S]+?)(?=\n\[\d{2}/\d{2}/\d{4}|\Z)"
    )

    matches = pattern.findall(content)

    for match in matches:
        timestamp_str, author, text = match

        if 'PROCESS REPORT' in text.upper():
            timestamp = datetime.strptime(timestamp_str, '%d/%m/%Y %H:%M')
            parse_report_block(reports, author, timestamp, text)

    return reports

def parse_report_block(reports, author, timestamp, text):
    report = {
        'author': author.strip(),
        'timestamp': timestamp,
        'processors': [],
    }

    text = text.replace('*', '').replace('🔹', '\n- ')

    keys = [
        'BATCH NUMBER', 'DATE', 'SHIFT', 'PROCESS START', 'HEATING DURATION', 'HEATING', 'KEEPING',
        'COOLING', 'END', 'NUMBER OF CAKE DRIED',
        'TECHNICAL CHALLENGE', 'MAINTENANCE', 'PROCESS DURATION', 'REMARKS'
    ]
    key_regex = r'(' + '|'.join(keys) + r')'

    # Use findall to get all key-value pairs
    pairs = re.findall(r'(' + '|'.join(keys) + r')\s*:?\s*(.*)', text, re.IGNORECASE)

    data = {key.strip().upper(): val.strip() for key, val in pairs}

    report['batch_number'] = data.get('BATCH NUMBER')
    if not report['batch_number']:
        return

    date_str_val = data.get('DATE')
    if date_str_val:
        date_str = date_str_val.split()[0]
        for fmt in ('%d/%m/%Y', '%d/%m/%y'):
            try:
                report['date'] = datetime.strptime(date_str, fmt).date()
                break
            except ValueError:
                continue
    if 'date' not in report:
        report['date'] = timestamp.date()

    report['shift'] = data.get('SHIFT')

    date = report.get('date')
    if date:
        report['process_start_dt'] = parse_time(data.get('PROCESS START'), date)
        report['heating_start_dt'] = parse_time(data.get('HEATING'), date, report.get('process_start_dt'))
        report['keeping_start_dt'] = parse_time(data.get('KEEPING'), date, report.get('heating_start_dt'))
        report['cooling_start_dt'] = parse_time(data.get('COOLING'), date, report.get('keeping_start_dt'))
        report['process_end_dt'] = parse_time(data.get('END'), date, report.get('cooling_start_dt'))

    report['heating_duration_minutes'] = parse_duration_to_minutes(data.get('HEATING DURATION'))
    report['process_duration_minutes'] = parse_duration_to_minutes(data.get('PROCESS DURATION'))

    cakes_str = data.get('NUMBER OF CAKE DRIED', '0')
    cakes_match = re.search(r'\d+', cakes_str)
    report['number_of_cakes_dried'] = int(cakes_match.group(0)) if cakes_match else 0

    report['technical_challenges'] = data.get('TECHNICAL CHALLENGE', 'N/A')
    report['maintenance_notes'] = data.get('MAINTENANCE', 'N/A')
    report['remarks'] = data.get('REMARKS', 'N/A')

    if 'PROCESS DONE BY' in text.upper():
        processors_text = text.upper().split('PROCESS DONE BY')[1]
        report['processors'] = [name.strip() for name in re.split(r'\n|-', processors_text) if name.strip() and 'PROCESS' not in name]
    elif any(name in text.upper() for name in ['AZEEZ KABIR', 'OLAYEMI OYENIYI', 'AFUYE OLATUNDE']):
         processors_list = [line.strip() for line in text.split('\n') if any(op_name in line.upper() for op_name in ['AZEEZ', 'OLAYEMI', 'AFUYE'])]
         report['processors'] = [p for p in processors_list if 'PROCESS' not in p]

    if report['batch_number'] not in reports or reports[report['batch_number']]['timestamp'] < report['timestamp']:
        reports[report['batch_number']] = report

def get_employee_id(name_or_phone, employee_map):
    if not name_or_phone: return None

    if name_or_phone.startswith('+'):
        phone_number = ''.join(filter(str.isdigit, name_or_phone))
        for num, emp_id in employee_map.items():
            if phone_number.endswith(num):
                return emp_id
    else:
        name = name_or_phone.lower().replace('mr', '').replace('.', '').strip()
        for emp_name, emp_id in employee_map.items():
            if not emp_name.isdigit() and name == emp_name.lower():
                return emp_id
        for emp_name, emp_id in employee_map.items():
            if not emp_name.isdigit() and all(part in emp_name.lower().split() for part in name.split()):
                return emp_id
    return None

def generate_sql(reports):
    employee_map = {
        'Emmanuel Olaoye': 1, 'olaoye e.a': 1, 'olaoye emmanuel': 1, '9060834296': 1,
        'Niyi Olayemi': 2, 'olayemi oyeniyi': 2, 'olayemi o.s': 2, '7062716844': 2,
        'Joel QC': 3, 'Joel Afuye': 3, 'Afuye Olatunde Joel': 3, 'afuye joel': 3, 'afuye olatunde': 3, '7066150893': 3,
        'Azeez Production Officer': 4, 'Azeez Kabir': 4, 'azeez k.l': 4, '8105931726': 4,
        'jubfuns': 5,
        'PrinceAjibola Abdulateef APM': 6,
        'Mr Dare Production Supervisor': 7, 'Dare Oloniruha': 7,
        'Mr Ibrahim Production Executive': 8, 'Ibrahim Opeyemi': 8,
        'Highbee': 9
    }

    sql_statements = []

    for batch_number, report in sorted(reports.items(), key=lambda item: item[1]['timestamp']):
        production_chemist_id = get_employee_id(report['author'], employee_map) or 'NULL'

        def sql_safe(value):
            if value is None:
                return 'NULL'
            if isinstance(value, (int, float)):
                return str(value)
            return f"'{str(value).replace("'", "''")}'"

        values = {
            'batch_number': sql_safe(report['batch_number']),
            'date': sql_safe(report['date'].strftime('%Y-%m-%d')) if report.get('date') else 'NULL',
            'shift': sql_safe(report.get('shift')),
            'production_chemist_employee_id': str(production_chemist_id),
            'process_start': sql_safe(report['process_start_dt'].strftime('%Y-%m-%d %H:%M:%S')) if report.get('process_start_dt') else 'NULL',
            'heating_start': sql_safe(report['heating_start_dt'].strftime('%Y-%m-%d %H:%M:%S')) if report.get('heating_start_dt') else 'NULL',
            'keeping_start': sql_safe(report['keeping_start_dt'].strftime('%Y-%m-%d %H:%M:%S')) if report.get('keeping_start_dt') else 'NULL',
            'cooling_start': sql_safe(report['cooling_start_dt'].strftime('%Y-%m-%d %H:%M:%S')) if report.get('cooling_start_dt') else 'NULL',
            'process_end': sql_safe(report['process_end_dt'].strftime('%Y-%m-%d %H:%M:%S')) if report.get('process_end_dt') else 'NULL',
            'heating_duration_minutes': sql_safe(report.get('heating_duration_minutes')),
            'process_duration_minutes': sql_safe(report.get('process_duration_minutes')),
            'number_of_cakes_dried': sql_safe(report.get('number_of_cakes_dried')),
            'technical_challenges': sql_safe(report.get('technical_challenges')),
            'maintenance_notes': sql_safe(report.get('maintenance_notes')),
            'remarks': sql_safe(report.get('remarks')),
        }

        cols = ', '.join(values.keys())
        vals = ', '.join(values.values())
        updates = ', '.join([f"{k}={v}" for k, v in values.items() if k != 'batch_number'])

        sql = f"INSERT INTO bleaching_process ({cols}) VALUES ({vals}) ON DUPLICATE KEY UPDATE {updates};\n"
        sql_statements.append(sql)

        processors = report.get('processors', [])
        if not processors:
            processors = [report['author']]

        for processor_name in processors:
            emp_id = get_employee_id(processor_name, employee_map)
            if emp_id:
                kier_sql = (f"INSERT IGNORE INTO kier_processors (batch_number, employee_id) "
                            f"VALUES ({sql_safe(report['batch_number'])}, {emp_id});\n")
                sql_statements.append(kier_sql)

    with open('data_population.sql', 'w', encoding='utf-8') as f:
        f.writelines(sql_statements)

if __name__ == '__main__':
    parsed_reports = parse_whatsapp_chat('whatsapp_chat.txt')
    generate_sql(parsed_reports)
    print(f"Generated data_population.sql successfully with {len(parsed_reports)} reports.")

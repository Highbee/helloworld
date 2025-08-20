import re
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError

# --- Helper functions ---

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

    text_upper = text.upper()

    keys = [
        'BATCH NUMBER', 'DATE', 'SHIFT', 'PROCESS START', 'HEATING DURATION', 'HEATING', 'KEEPING',
        'COOLING', 'END', 'NUMBER OF CAKE DRIED',
        'TECHNICAL CHALLENGE', 'MAINTENANCE', 'PROCESS DURATION', 'REMARKS'
    ]
    key_regex = r'(' + '|'.join(keys) + r')'

    parts = re.split(key_regex, text, flags=re.IGNORECASE)

    data = {}
    remaining_text = ''
    if len(parts) > 1:
        remaining_text = parts[0]
        for i in range(1, len(parts), 2):
            key = parts[i].strip().upper()
            value_block = parts[i+1]

            value_lines = value_block.strip().split('\n')
            value = ' '.join(v.replace(':', '').strip() for v in value_lines)
            data[key] = value

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

    processors_text = ""
    if 'PROCESS DONE BY' in text_upper:
        processors_text = text_upper.split('PROCESS DONE BY')[1]
    elif any(name in text_upper for name in ['AZEEZ KABIR', 'OLAYEMI OYENIYI', 'AFUYE OLATUNDE']):
         processors_text = '\n'.join([line for line in text.split('\n') if any(op_name in line.upper() for op_name in ['AZEEZ', 'OLAYEMI', 'AFUYE'])])

    if processors_text:
        report['processors'] = [name.strip() for name in re.split(r'\n|-|🔹', processors_text) if name.strip() and 'PROCESS' not in name.upper()]

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

def generate_sql(reports, output_file):
    employee_map = {
        'Emmanuel Olaoye': 1, 'olaoye e.a': 1, 'olaoye emmanuel': 1, '9060834296': 1,
        'Niyi Olayemi': 2, 'olayemi oyeniyi': 2, 'olayemi o.s': 2, '7062716844': 2,
        'Joel Afuye': 3, 'afuye olatunde joel': 3, 'afuye joel': 3, 'afuye olatunde': 3, '7066150893': 3,
        'Azeez Kabir': 4, 'azeez k.l': 4, '8105931726': 4,
        'jubfuns': 5,
        'PrinceAjibola Abdulateef APM': 6,
        'Mr Dare Production Supervisor': 7, 'Dare Oloniruha': 7,
        'Mr Ibrahim Production Executive': 8, 'Ibrahim Opeyemi': 8,
        'Highbee': 9
    }
    bleaching_operator_ids = {1, 2, 3, 4}

    sql_statements = []

    for batch_number, report in sorted(reports.items(), key=lambda item: item[1]['timestamp']):
        author_id = get_employee_id(report['author'], employee_map)

        processors = []
        if report.get('processors'):
            processors = [get_employee_id(p, employee_map) for p in report['processors']]
        elif author_id in bleaching_operator_ids:
            processors = [author_id]

        processors = [p for p in processors if p is not None and p in bleaching_operator_ids]

        production_chemist_id = processors[0] if processors else 'NULL'

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

        for emp_id in processors:
            kier_sql = (f"INSERT IGNORE INTO kier_processors (batch_number, employee_id) "
                        f"VALUES ({sql_safe(report['batch_number'])}, {emp_id});\n")
            sql_statements.append(kier_sql)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(sql_statements)

class Command(BaseCommand):
    help = 'Parses a WhatsApp chat log to generate an SQL file for populating bleaching process data.'

    def add_arguments(self, parser):
        parser.add_argument('chat_file', type=str, help='The path to the WhatsApp chat log file.')
        parser.add_argument('output_sql_file', type=str, help='The path to the output SQL file.')

    def handle(self, *args, **options):
        chat_file_path = options['chat_file']
        output_sql_path = options['output_sql_file']

        try:
            parsed_reports = parse_whatsapp_chat(chat_file_path)
            generate_sql(parsed_reports, output_sql_path)
            self.stdout.write(self.style.SUCCESS(f"Generated {output_sql_path} successfully with {len(parsed_reports)} reports."))
        except FileNotFoundError:
            raise CommandError(f'File not found at "{chat_file_path}"')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')

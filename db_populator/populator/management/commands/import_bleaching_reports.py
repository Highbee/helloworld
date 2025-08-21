import re
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from populator.models import BleachingProcess, Employees, KierProcessors

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
    if len(parts) > 1:
        for i in range(1, len(parts), 2):
            key = parts[i].strip().upper()
            value = parts[i+1].replace(':', '').strip()
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

def get_employee(name_or_phone, employee_map):
    if not name_or_phone: return None

    if name_or_phone.startswith('+'):
        phone_number = ''.join(filter(str.isdigit, name_or_phone))
        for num, emp_id in employee_map.items():
            if phone_number.endswith(num):
                return Employees.objects.filter(pk=emp_id).first()
    else:
        name = name_or_phone.lower().replace('mr', '').replace('.', '').strip()
        for emp_name, emp_id in employee_map.items():
            if not emp_name.isdigit() and name == emp_name.lower():
                return Employees.objects.filter(pk=emp_id).first()
        for emp_name, emp_id in employee_map.items():
            if not emp_name.isdigit() and all(part in emp_name.lower().split() for part in name.split()):
                return Employees.objects.filter(pk=emp_id).first()
    return None

class Command(BaseCommand):
    help = 'Parses a WhatsApp chat log to populate bleaching process data using the Django ORM.'

    def add_arguments(self, parser):
        parser.add_argument('chat_file', type=str, help='The path to the WhatsApp chat log file.')

    def handle(self, *args, **options):
        chat_file_path = options['chat_file']

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

        try:
            parsed_reports = parse_whatsapp_chat(chat_file_path)

            for batch_number, report_data in parsed_reports.items():
                author_employee = get_employee(report_data['author'], employee_map)

                processors = []
                if report_data.get('processors'):
                    processors = [get_employee(p, employee_map) for p in report_data['processors']]
                elif author_employee and author_employee.pk in bleaching_operator_ids:
                    processors = [author_employee]

                processors = [p for p in processors if p is not None and p.pk in bleaching_operator_ids]

                production_chemist = processors[0] if processors else None

                defaults = {
                    'date': report_data.get('date'),
                    'shift': report_data.get('shift'),
                    'production_chemist_employee': production_chemist,
                    'process_start': report_data.get('process_start_dt'),
                    'heating_start': report_data.get('heating_start_dt'),
                    'keeping_start': report_data.get('keeping_start_dt'),
                    'cooling_start': report_data.get('cooling_start_dt'),
                    'process_end': report_data.get('process_end_dt'),
                    'heating_duration_minutes': report_data.get('heating_duration_minutes'),
                    'process_duration_minutes': report_data.get('process_duration_minutes'),
                    'number_of_cakes_dried': report_data.get('number_of_cakes_dried'),
                    'technical_challenges': report_data.get('technical_challenges'),
                    'maintenance_notes': report_data.get('maintenance_notes'),
                    'remarks': report_data.get('remarks'),
                }

                process, created = BleachingProcess.objects.update_or_create(
                    batch_number=batch_number,
                    defaults=defaults
                )

                if processors:
                    process.processors.set(processors)

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created new process for batch {batch_number}'))
                else:
                    self.stdout.write(self.style.SUCCESS(f'Updated process for batch {batch_number}'))

            self.stdout.write(self.style.SUCCESS(f"Successfully processed {len(parsed_reports)} reports."))

        except FileNotFoundError:
            raise CommandError(f'File not found at "{chat_file_path}"')
        except Exception as e:
            raise CommandError(f'An error occurred: {e}')

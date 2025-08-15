from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import JsonResponse
import json
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from .models import Employees, Products, Status, Productions, BleachingProcess, Transfers, TransferItems
from .forms import EmployeeForm, ProductForm, StatusForm, ProductionsForm, BleachingProcessForm, TransfersForm, ProductionFormSet, TransferItemsFormSet, BatchReportForm, DateRangeReportForm

def employee_list(request):
    employees = Employees.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'employee_form.html', {'form': form})

def product_list(request):
    products = Products.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

def status_list(request):
    statuses = Status.objects.all()
    return render(request, 'status_list.html', {'statuses': statuses})

def status_add(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('status_list')
    else:
        form = StatusForm()
    return render(request, 'status_form.html', {'form': form})

def home(request):
    return render(request, 'home.html')

def productions_list(request):
    productions = Productions.objects.select_related('product', 'supervisor_employee').all()

    # Filtering
    product_filter = request.GET.get('product')
    supervisor_filter = request.GET.get('supervisor')
    date_after_filter = request.GET.get('date_after')
    date_before_filter = request.GET.get('date_before')
    shift_filter = request.GET.get('shift')
    line_filter = request.GET.get('line')

    if product_filter:
        productions = productions.filter(product__product_id=product_filter)
    if supervisor_filter:
        productions = productions.filter(supervisor_employee__employee_id=supervisor_filter)
    if date_after_filter:
        productions = productions.filter(date__gte=date_after_filter)
    if date_before_filter:
        productions = productions.filter(date__lte=date_before_filter)
    if shift_filter:
        productions = productions.filter(shift__icontains=shift_filter)
    if line_filter:
        productions = productions.filter(production_line__icontains=line_filter)

    # Sorting
    sort_by = request.GET.get('sort', 'production_id')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = f'-{sort_by}'
    productions = productions.order_by(sort_by)

    context = {
        'productions': productions,
        'products': Products.objects.all(),
        'supervisors': Employees.objects.filter(status__status_name='Supervisor'),
        'filter_values': request.GET,
        'sort_by': request.GET.get('sort', 'production_id'),
        'order': request.GET.get('order', 'asc'),
    }
    return render(request, 'productions_list.html', context)

def productions_add(request):
    if request.method == 'POST':
        form = ProductionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productions_list')
    else:
        form = ProductionsForm()

    supervisors = Employees.objects.filter(status__status_name='Supervisor')
    supervisors_json = json.dumps({
        s.employee_id: f'{s.first_name} {s.last_name}' for s in supervisors
    })

    return render(request, 'productions_form.html', {
        'form': form,
        'supervisors_json': supervisors_json,
    })

def bleaching_process_list(request):
    bleaching_processes = BleachingProcess.objects.select_related('production_chemist_employee').all()

    # Filtering
    chemist_filter = request.GET.get('chemist')
    date_after_filter = request.GET.get('date_after')
    date_before_filter = request.GET.get('date_before')
    shift_filter = request.GET.get('shift')

    if chemist_filter:
        bleaching_processes = bleaching_processes.filter(production_chemist_employee__employee_id=chemist_filter)
    if date_after_filter:
        bleaching_processes = bleaching_processes.filter(date__gte=date_after_filter)
    if date_before_filter:
        bleaching_processes = bleaching_processes.filter(date__lte=date_before_filter)
    if shift_filter:
        bleaching_processes = bleaching_processes.filter(shift__icontains=shift_filter)

    # Sorting
    sort_by = request.GET.get('sort', 'idbleaching_process')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = f'-{sort_by}'
    bleaching_processes = bleaching_processes.order_by(sort_by)

    context = {
        'bleaching_processes': bleaching_processes,
        'chemists': Employees.objects.filter(status__status_name='Chemist'),
        'filter_values': request.GET,
        'sort_by': request.GET.get('sort', 'idbleaching_process'),
        'order': request.GET.get('order', 'asc'),
    }
    return render(request, 'bleaching_process_list.html', context)

def bleaching_process_add(request):
    if request.method == 'POST':
        form = BleachingProcessForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bleaching_process_list')
    else:
        form = BleachingProcessForm()
    return render(request, 'bleaching_process_form.html', {'form': form})

def transfers_list(request):
    transfers = Transfers.objects.select_related('supervisor_employee').all()

    # Filtering
    supervisor_filter = request.GET.get('supervisor')
    date_after_filter = request.GET.get('date_after')
    date_before_filter = request.GET.get('date_before')
    line_filter = request.GET.get('line')

    if supervisor_filter:
        transfers = transfers.filter(supervisor_employee__employee_id=supervisor_filter)
    if date_after_filter:
        transfers = transfers.filter(date__gte=date_after_filter)
    if date_before_filter:
        transfers = transfers.filter(date__lte=date_before_filter)
    if line_filter:
        transfers = transfers.filter(production_line__icontains=line_filter)

    # Sorting
    sort_by = request.GET.get('sort', 'transfer_id')
    order = request.GET.get('order', 'asc')
    if order == 'desc':
        sort_by = f'-{sort_by}'
    transfers = transfers.order_by(sort_by)

    context = {
        'transfers': transfers,
        'supervisors': Employees.objects.filter(status__status_name='Supervisor'),
        'filter_values': request.GET,
        'sort_by': request.GET.get('sort', 'transfer_id'),
        'order': request.GET.get('order', 'asc'),
    }
    return render(request, 'transfers_list.html', context)

def transfers_add(request):
    if request.method == 'POST':
        form = TransfersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transfers_list')
    else:
        form = TransfersForm()
    return render(request, 'transfers_form.html', {'form': form})

def production_vs_transfers_checker(request):
    # Get total production per product per day
    production_by_day = Productions.objects.values('date', 'product__product_name').annotate(total_produced=Sum('quantity_produced')).order_by('date', 'product__product_name')

    # Get total transfers per product per day
    transfers_by_day = TransferItems.objects.values('transfer__date', 'product__product_name').annotate(total_transferred=Sum('quantity_transferred')).order_by('transfer__date', 'product__product_name')

    # Create a dictionary for easier lookup
    production_dict = {}
    for p in production_by_day:
        key = (p['date'], p['product__product_name'])
        production_dict[key] = p['total_produced']

    transfers_dict = {}
    for t in transfers_by_day:
        key = (t['transfer__date'], t['product__product_name'])
        transfers_dict[key] = t['total_transferred']

    # Find discrepancies
    discrepancies = []
    all_keys = sorted(list(set(production_dict.keys()) | set(transfers_dict.keys())))

    for key in all_keys:
        date, product_name = key
        produced = production_dict.get(key, 0)
        transferred = transfers_dict.get(key, 0)
        if produced != transferred:
            discrepancies.append({
                'date': date,
                'product_name': product_name,
                'produced': produced,
                'transferred': transferred,
                'difference': produced - transferred,
            })

    context = {
        'discrepancies': discrepancies,
    }
    return render(request, 'production_vs_transfers_checker.html', context)

def api_daily_production(request):
    productions = Productions.objects.all()

    # Filtering
    product_filter = request.GET.get('product')
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')

    if product_filter:
        productions = productions.filter(product__product_id=product_filter)
    if start_date_filter:
        productions = productions.filter(date__gte=start_date_filter)
    if end_date_filter:
        productions = productions.filter(date__lte=end_date_filter)

    production_by_day = productions.annotate(day=TruncDay('date')).values('day', 'product__product_name').annotate(total_produced=Sum('quantity_produced')).order_by('day')

    # Convert date objects to strings for JSON serialization
    for item in production_by_day:
        item['day'] = item['day'].strftime('%Y-%m-%d')

    return JsonResponse(list(production_by_day), safe=False)

def api_weekly_production(request):
    productions = Productions.objects.all()

    # Filtering
    product_filter = request.GET.get('product')
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')

    if product_filter:
        productions = productions.filter(product__product_id=product_filter)
    if start_date_filter:
        productions = productions.filter(date__gte=start_date_filter)
    if end_date_filter:
        productions = productions.filter(date__lte=end_date_filter)

    production_by_week = productions.annotate(week=TruncWeek('date')).values('week', 'product__product_name').annotate(total_produced=Sum('quantity_produced')).order_by('week')

    for item in production_by_week:
        item['week'] = item['week'].strftime('%Y-%m-%d')

    return JsonResponse(list(production_by_week), safe=False)

def api_monthly_production(request):
    productions = Productions.objects.all()

    # Filtering
    product_filter = request.GET.get('product')
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')

    if product_filter:
        productions = productions.filter(product__product_id=product_filter)
    if start_date_filter:
        productions = productions.filter(date__gte=start_date_filter)
    if end_date_filter:
        productions = productions.filter(date__lte=end_date_filter)

    production_by_month = productions.annotate(month=TruncMonth('date')).values('month', 'product__product_name').annotate(total_produced=Sum('quantity_produced')).order_by('month')

    for item in production_by_month:
        item['month'] = item['month'].strftime('%Y-%m')

    return JsonResponse(list(production_by_month), safe=False)

def infographics_dashboard(request):
    context = {
        'products': Products.objects.all(),
    }
    return render(request, 'infographics_dashboard.html', context)

def productions_formset_view(request):
    if request.method == 'POST':
        formset = ProductionFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('productions_list')
    else:
        formset = ProductionFormSet(queryset=Productions.objects.none())

    supervisors = Employees.objects.filter(status__status_name='Supervisor')
    supervisors_json = json.dumps({
        s.employee_id: f'{s.first_name} {s.last_name}' for s in supervisors
    })

    return render(request, 'productions_formset.html', {
        'formset': formset,
        'supervisors_json': supervisors_json,
    })

def transfers_inline_formset_view(request):
    if request.method == 'POST':
        form = TransfersForm(request.POST)
        if form.is_valid():
            transfer_instance = form.save(commit=False)
            formset = TransferItemsFormSet(request.POST, instance=transfer_instance)
            if formset.is_valid():
                transfer_instance.save()
                formset.save()
                return redirect('transfers_list')
    else:
        form = TransfersForm()
        formset = TransferItemsFormSet(queryset=TransferItems.objects.none())

    return render(request, 'transfers_inline_formset.html', {'form': form, 'formset': formset})

def reports_index(request):
    batch_form = BatchReportForm()
    date_range_form = DateRangeReportForm()
    context = {
        'batch_form': batch_form,
        'date_range_form': date_range_form,
    }
    return render(request, 'reports_index.html', context)

def report_batch_production(request):
    batch_number = request.GET.get('batch_number')
    report_data = []
    if batch_number:
        report_data = Productions.objects.filter(batch_number=batch_number)\
            .values('product__product_name', 'batch_number')\
            .annotate(total_produced=Sum('quantity_produced'))\
            .order_by('product__product_name')

    context = {
        'report_data': report_data,
        'batch_number': batch_number,
    }
    return render(request, 'report_batch_production.html', context)

def report_daily_transfer_details(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    report_data = []
    if start_date and end_date:
        report_data = TransferItems.objects.filter(transfer__date__range=[start_date, end_date])\
            .select_related('transfer__supervisor_employee', 'product')\
            .order_by('transfer__date', 'product__product_name')

    context = {
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'report_daily_transfer_details.html', context)

def report_supervisor_transfer_summary(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    report_data = []
    if start_date and end_date:
        report_data = TransferItems.objects.filter(transfer__date__range=[start_date, end_date])\
            .values('transfer__date', 'product__product_name', 'transfer__supervisor_employee__last_name')\
            .annotate(total_transferred=Sum('quantity_transferred'))\
            .order_by('transfer__date', 'transfer__supervisor_employee__last_name', 'product__product_name')

    context = {
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'report_supervisor_transfer_summary.html', context)

def report_daily_transfer_summary(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    report_data = []
    if start_date and end_date:
        report_data = TransferItems.objects.filter(transfer__date__range=[start_date, end_date])\
            .values('transfer__date', 'product__product_name')\
            .annotate(total_transferred=Sum('quantity_transferred'))\
            .order_by('transfer__date', 'product__product_name')

    context = {
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'report_daily_transfer_summary.html', context)

def report_total_production(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    report_data = []
    if start_date and end_date:
        report_data = Productions.objects.filter(date__range=[start_date, end_date])\
            .values('product__product_name')\
            .annotate(total_produced=Sum('quantity_produced'))\
            .order_by('product__product_name')

    context = {
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'report_total_production.html', context)

def report_total_transfer_summary(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    report_data = []
    if start_date and end_date:
        report_data = TransferItems.objects.filter(transfer__date__range=[start_date, end_date])\
            .values('product__product_name')\
            .annotate(total_transferred=Sum('quantity_transferred'))\
            .order_by('product__product_name')

    context = {
        'report_data': report_data,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'report_total_transfer_summary.html', context)

from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import JsonResponse
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from .models import Employees, Products, Status, Productions, BleachingProcess, Transfers, TransferItems
from .forms import EmployeeForm, ProductForm, StatusForm, ProductionsForm, BleachingProcessForm, TransfersForm, ProductionFormSet, TransferItemsFormSet

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
    productions = Productions.objects.all()
    return render(request, 'productions_list.html', {'productions': productions})

def productions_add(request):
    if request.method == 'POST':
        form = ProductionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productions_list')
    else:
        form = ProductionsForm()
    return render(request, 'productions_form.html', {'form': form})

def bleaching_process_list(request):
    bleaching_processes = BleachingProcess.objects.all()
    return render(request, 'bleaching_process_list.html', {'bleaching_processes': bleaching_processes})

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
    transfers = Transfers.objects.all()
    return render(request, 'transfers_list.html', {'transfers': transfers})

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
    production_by_day = Productions.objects.annotate(day=TruncDay('date')).values('day', 'product__product_name').annotate(total_produced=Sum('quantity_produced')).order_by('day')

    # Convert date objects to strings for JSON serialization
    for item in production_by_day:
        item['day'] = item['day'].strftime('%Y-%m-%d')

    return JsonResponse(list(production_by_day), safe=False)

def api_weekly_production(request):
    production_by_week = Productions.objects.annotate(week=TruncWeek('date')).values('week', 'product__product_name').annotate(total_produced=Sum('quantity_produced')).order_by('week')

    for item in production_by_week:
        item['week'] = item['week'].strftime('%Y-%m-%d')

    return JsonResponse(list(production_by_week), safe=False)

def api_monthly_production(request):
    production_by_month = Productions.objects.annotate(month=TruncMonth('date')).values('month', 'product__product_name').annotate(total_produced=Sum('quantity_produced')).order_by('month')

    for item in production_by_month:
        item['month'] = item['month'].strftime('%Y-%m')

    return JsonResponse(list(production_by_month), safe=False)

def infographics_dashboard(request):
    return render(request, 'infographics_dashboard.html')

def productions_formset_view(request):
    if request.method == 'POST':
        formset = ProductionFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.has_changed(): # This ignores empty forms
                    form.save()
            return redirect('productions_list') # Or a new success page
    else:
        formset = ProductionFormSet(queryset=Productions.objects.none()) # Start with an empty formset

    return render(request, 'productions_formset.html', {'formset': formset})

def transfers_inline_formset_view(request):
    if request.method == 'POST':
        form = TransfersForm(request.POST)
        formset = TransferItemsFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            transfer_instance = form.save()
            formset.instance = transfer_instance
            formset.save()
            return redirect('transfers_list')
    else:
        form = TransfersForm()
        formset = TransferItemsFormSet(queryset=TransferItems.objects.none())

    return render(request, 'transfers_inline_formset.html', {'form': form, 'formset': formset})

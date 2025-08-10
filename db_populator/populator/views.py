from django.shortcuts import render, redirect
from .models import Employees, Products, Status, Productions, BleachingProcess, Transfers
from .forms import EmployeeForm, ProductForm, StatusForm, ProductionsForm, BleachingProcessForm, TransfersForm

def employee_list(request):
    employees = Employees.objects.all()
    return render(request, 'populator/employee_list.html', {'employees': employees})

def employee_add(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'populator/employee_form.html', {'form': form})

def product_list(request):
    products = Products.objects.all()
    return render(request, 'populator/product_list.html', {'products': products})

def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'populator/product_form.html', {'form': form})

def status_list(request):
    statuses = Status.objects.all()
    return render(request, 'populator/status_list.html', {'statuses': statuses})

def status_add(request):
    if request.method == 'POST':
        form = StatusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('status_list')
    else:
        form = StatusForm()
    return render(request, 'populator/status_form.html', {'form': form})

def home(request):
    return render(request, 'populator/home.html')

def productions_list(request):
    productions = Productions.objects.all()
    return render(request, 'populator/productions_list.html', {'productions': productions})

def productions_add(request):
    if request.method == 'POST':
        form = ProductionsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productions_list')
    else:
        form = ProductionsForm()
    return render(request, 'populator/productions_form.html', {'form': form})

def bleaching_process_list(request):
    bleaching_processes = BleachingProcess.objects.all()
    return render(request, 'populator/bleaching_process_list.html', {'bleaching_processes': bleaching_processes})

def bleaching_process_add(request):
    if request.method == 'POST':
        form = BleachingProcessForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('bleaching_process_list')
    else:
        form = BleachingProcessForm()
    return render(request, 'populator/bleaching_process_form.html', {'form': form})

def transfers_list(request):
    transfers = Transfers.objects.all()
    return render(request, 'populator/transfers_list.html', {'transfers': transfers})

def transfers_add(request):
    if request.method == 'POST':
        form = TransfersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transfers_list')
    else:
        form = TransfersForm()
    return render(request, 'populator/transfers_form.html', {'form': form})

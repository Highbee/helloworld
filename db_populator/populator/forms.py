from django import forms
from datetime import date, datetime
from .models import Employees, Products, Status, Productions, BleachingProcess, Transfers, FactoryUnit

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employees
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'

class ProductionsForm(forms.ModelForm):
    class Meta:
        model = Productions
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today

class BleachingProcessForm(forms.ModelForm):
    class Meta:
        model = BleachingProcess
        fields = '__all__'
        widgets = {
            'processors': forms.CheckboxSelectMultiple,
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['processors'].queryset = Employees.objects.filter(unit__unit_name='Bleaching')
        self.fields['date'].initial = date.today

class TransfersForm(forms.ModelForm):
    class Meta:
        model = Transfers
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'transfer_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = date.today
        self.fields['transfer_time'].initial = datetime.now().strftime('%H:%M')

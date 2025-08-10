from django import forms
from .models import Employees, Products, Status, Productions, BleachingProcess, Transfers

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

class BleachingProcessForm(forms.ModelForm):
    class Meta:
        model = BleachingProcess
        fields = '__all__'

class TransfersForm(forms.ModelForm):
    class Meta:
        model = Transfers
        fields = '__all__'

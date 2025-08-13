from django import forms
from datetime import date, datetime
from .models import Employees, Products, Status, Productions, BleachingProcess, Transfers, FactoryUnit, TransferItems

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

ProductionFormSet = forms.modelformset_factory(
    Productions,
    form=ProductionsForm,
    extra=1,
    can_delete=True
)

class BatchReportForm(forms.Form):
    batch_number = forms.CharField(label="Batch Number", max_length=10)

class DateRangeReportForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class TransferItemsForm(forms.ModelForm):
    class Meta:
        model = TransferItems
        fields = ['product', 'quantity_transferred']

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity_transferred')

        # This validation logic is not perfect, because it doesn't account for the `DELETE` checkbox.
        # A better approach is to only validate if the form has changed.
        # However, for now, this is a good start.
        if product and not quantity:
            self.add_error('quantity_transferred', 'This field is required when a product is selected.')

        if quantity and not product:
            self.add_error('product', 'This field is required when a quantity is entered.')

        return cleaned_data

TransferItemsFormSet = forms.inlineformset_factory(
    Transfers,
    TransferItems,
    form=TransferItemsForm,
    extra=1,
    can_delete=True
)

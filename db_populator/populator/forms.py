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

        # If the form is marked for deletion, no further validation is needed.
        if self.cleaned_data.get('DELETE'):
            return cleaned_data

        # If the form is empty and hasn't been touched, it's valid.
        # The formset will know not to save it.
        if not self.has_changed():
            return cleaned_data

        # At this point, the form has changed, so we expect valid data.
        product = cleaned_data.get('product')
        quantity = cleaned_data.get('quantity_transferred')

        if not product:
            self.add_error('product', 'This field is required when entering a transfer item.')

        if quantity is None: # Check for None because quantity can be 0
            self.add_error('quantity_transferred', 'This field is required when entering a transfer item.')

        return cleaned_data

TransferItemsFormSet = forms.inlineformset_factory(
    Transfers,
    TransferItems,
    form=TransferItemsForm,
    extra=1,
    can_delete=True
)

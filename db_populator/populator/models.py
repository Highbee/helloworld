from django.db import models

class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=45)

    def __str__(self):
        return self.status_name

    class Meta:
        db_table = 'status'
        verbose_name_plural = 'statuses'

class FactoryUnit(models.Model):
    unit_id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.unit_name

    class Meta:
        db_table = 'factory_unit'
        verbose_name_plural = 'factory units'

class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT, db_column='status_id')
    unit = models.ForeignKey(FactoryUnit, on_delete=models.SET_NULL, null=True, blank=True, db_column='unit_id')
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    gender = models.CharField(max_length=1)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'employees'
        verbose_name_plural = 'employees'

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=55)
    packaging_units = models.CharField(max_length=10)
    number_of_units_per_pack = models.IntegerField()

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'products'
        verbose_name_plural = 'products'

class BleachingProcess(models.Model):
    idbleaching_process = models.AutoField(primary_key=True)
    production_chemist_employee = models.ForeignKey(Employees, on_delete=models.RESTRICT, related_name='bleaching_processes_as_chemist', db_column='production_chemist_employee_id')
    batch_number = models.CharField(max_length=9, unique=True, blank=True, null=True)
    date = models.DateField()
    shift = models.CharField(max_length=9)
    comments = models.CharField(max_length=255)
    number_of_cakes_to_rebleached = models.IntegerField()
    number_of_rebleach_added = models.IntegerField()
    processors = models.ManyToManyField(Employees, through='KierProcessors', related_name='bleaching_processes_as_processor')

    def __str__(self):
        return self.batch_number

    class Meta:
        db_table = 'bleaching_process'
        verbose_name_plural = 'bleaching processes'

class KierProcessors(models.Model):
    batch_number = models.ForeignKey(BleachingProcess, on_delete=models.RESTRICT, db_column='batch_number', to_field='batch_number')
    employee = models.ForeignKey(Employees, on_delete=models.RESTRICT, db_column='employee_id')

    class Meta:
        db_table = 'kier_processors'
        unique_together = (('batch_number', 'employee'),)
        verbose_name_plural = 'kier processors'

class Productions(models.Model):
    production_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.RESTRICT, db_column='product_id')
    supervisor_employee = models.ForeignKey(Employees, on_delete=models.RESTRICT, db_column='supervisor_employee_id')
    date = models.DateField()
    batch_number = models.CharField(max_length=10)
    shift = models.CharField(max_length=15, default='NA')
    production_line = models.CharField(max_length=1)
    quantity_produced = models.IntegerField()
    packaging_supervisor = models.CharField(max_length=45)
    notes = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.batch_number

    class Meta:
        db_table = 'productions'
        verbose_name_plural = 'productions'

class Transfers(models.Model):
    transfer_id = models.AutoField(primary_key=True)
    supervisor_employee = models.ForeignKey(Employees, on_delete=models.RESTRICT, db_column='supervisor_employee_id')
    date = models.DateField()
    transfer_time = models.TimeField()
    production_line = models.CharField(max_length=1)
    notes = models.CharField(max_length=750, blank=True, null=True)
    products = models.ManyToManyField(Products, through='TransferItems')

    def __str__(self):
        return str(self.transfer_id)

    class Meta:
        db_table = 'transfers'
        verbose_name_plural = 'transfers'

class TransferItems(models.Model):
    transfer = models.ForeignKey(Transfers, on_delete=models.RESTRICT, db_column='transfer_id')
    product = models.ForeignKey(Products, on_delete=models.RESTRICT, db_column='product_id')
    quantity_transferred = models.IntegerField()

    class Meta:
        db_table = 'transfer_items'
        unique_together = (('transfer', 'product'),)
        verbose_name_plural = 'transfer items'

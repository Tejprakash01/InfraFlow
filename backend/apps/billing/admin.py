from django.contrib import admin
from .models import Measurement, Bill, BillItem

@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('project', 'boq_item', 'measurement_date', 'current_quantity', 'verifier')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'project', 'net_amount', 'status', 'submitted_by')

@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ('bill', 'boq_item', 'current_quantity', 'rate', 'current_amount')

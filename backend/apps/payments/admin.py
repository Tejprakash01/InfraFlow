from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_reference', 'bill', 'amount', 'payment_status', 'utr_number', 'payment_date')

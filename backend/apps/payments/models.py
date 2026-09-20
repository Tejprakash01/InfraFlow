import uuid
from django.db import models

class PaymentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending Sanction'
    SANCTIONED = 'SANCTIONED', 'Payment Sanctioned'
    DISBURSED = 'DISBURSED', 'Payment Disbursed'
    FAILED = 'FAILED', 'Payment Failed'

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill = models.OneToOneField('billing.Bill', on_delete=models.CASCADE, related_name='payment')
    payment_reference = models.CharField(max_length=100, unique=True)
    utr_number = models.CharField(max_length=100, blank=True, default='')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    remarks = models.TextField(blank=True, default='')
    processed_by = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_reference} for Bill {self.bill.bill_number} - ₹{self.amount}"

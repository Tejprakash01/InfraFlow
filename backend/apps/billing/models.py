import uuid
from django.db import models

class BillStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    SUBMITTED = 'SUBMITTED', 'Submitted by Contractor'
    COMPLETENESS_CHECK = 'COMPLETENESS_CHECK', 'Document Completeness Check'
    RETURNED = 'RETURNED', 'Returned for Corrections'
    MEASUREMENT_VERIFICATION = 'MEASUREMENT_VERIFICATION', 'Measurement Verification'
    TECHNICAL_VERIFICATION = 'TECHNICAL_VERIFICATION', 'Technical Scrutiny'
    CERTIFIED = 'CERTIFIED', 'Engineer Certified'
    FINANCE_REVIEW = 'FINANCE_REVIEW', 'Finance / Accounts Review'
    AUTHORITY_APPROVAL = 'AUTHORITY_APPROVAL', 'Competent Authority Sanction'
    PAYMENT_PROCESSING = 'PAYMENT_PROCESSING', 'Payment Processing'
    PAID = 'PAID', 'Payment Completed / Paid'
    REJECTED = 'REJECTED', 'Bill Rejected'

class Measurement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='measurements')
    boq_item = models.ForeignKey('projects.BOQItem', on_delete=models.CASCADE, related_name='measurements')
    measurement_date = models.DateField()
    previous_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0.000)
    current_quantity = models.DecimalField(max_digits=12, decimal_places=3)
    cumulative_quantity = models.DecimalField(max_digits=12, decimal_places=3)
    balance_quantity = models.DecimalField(max_digits=12, decimal_places=3)
    verifier = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.project_code} - {self.boq_item.item_code}: {self.current_quantity} {self.boq_item.unit}"

class Bill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill_number = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='bills')
    government_file = models.OneToOneField('files.GovernmentFile', on_delete=models.SET_NULL, null=True, blank=True, related_name='linked_bill')
    
    bill_period_start = models.DateField()
    bill_period_end = models.DateField()
    
    gross_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    deductions_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    net_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    status = models.CharField(max_length=30, choices=BillStatus.choices, default=BillStatus.SUBMITTED)
    submitted_by = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.bill_number} - Net ₹{self.net_amount} ({self.status})"

class BillItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='items')
    boq_item = models.ForeignKey('projects.BOQItem', on_delete=models.RESTRICT)
    current_quantity = models.DecimalField(max_digits=12, decimal_places=3)
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.bill.bill_number} - {self.boq_item.item_code}"

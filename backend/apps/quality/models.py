import uuid
from django.db import models

class InspectionResult(models.TextChoices):
    PASS = 'PASS', 'Pass'
    FAIL = 'FAIL', 'Fail'
    RETURN = 'RETURN', 'Return for Correction'

class RFIStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Draft'
    SUBMITTED = 'SUBMITTED', 'Submitted'
    UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
    INSPECTION_SCHEDULED = 'INSPECTION_SCHEDULED', 'Inspection Scheduled'
    INSPECTED = 'INSPECTED', 'Inspected'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'
    CLOSED = 'CLOSED', 'Closed'

class NCRSeverity(models.TextChoices):
    MINOR = 'MINOR', 'Minor Defect'
    MAJOR = 'MAJOR', 'Major Non-Conformance'
    CRITICAL = 'CRITICAL', 'Critical Failure'

class NCRStatus(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    RESPONSE_SUBMITTED = 'RESPONSE_SUBMITTED', 'Corrective Action Submitted'
    VERIFIED = 'VERIFIED', 'Verified'
    CLOSED = 'CLOSED', 'Closed'

class SiteInspection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='inspections')
    inspection_date = models.DateField()
    inspector = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    location = models.CharField(max_length=255)
    work_package = models.ForeignKey('projects.WorkPackage', on_delete=models.SET_NULL, null=True, blank=True)
    observations = models.TextField()
    result = models.CharField(max_length=20, choices=InspectionResult.choices, default=InspectionResult.PASS)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.project_code} - Inspection on {self.inspection_date} ({self.result})"

class RFI(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfi_number = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='rfis')
    work_package = models.ForeignKey('projects.WorkPackage', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(max_length=255)
    requested_date = models.DateTimeField()
    description = models.TextField()
    status = models.CharField(max_length=30, choices=RFIStatus.choices, default=RFIStatus.SUBMITTED)
    created_by = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rfi_number} - {self.location}"

class NCR(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ncr_number = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='ncrs')
    location = models.CharField(max_length=255)
    work_package = models.ForeignKey('projects.WorkPackage', on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField()
    specification_breached = models.CharField(max_length=255, blank=True, default='')
    severity = models.CharField(max_length=20, choices=NCRSeverity.choices, default=NCRSeverity.MINOR)
    corrective_action_required = models.TextField()
    status = models.CharField(max_length=30, choices=NCRStatus.choices, default=NCRStatus.OPEN)
    due_date = models.DateField()
    created_by = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ncr_number} ({self.severity}) - {self.location}"

class Variation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    variation_number = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='variations')
    file = models.ForeignKey('files.GovernmentFile', on_delete=models.SET_NULL, null=True, blank=True, related_name='variations')
    description = models.TextField()
    proposed_quantity = models.DecimalField(max_digits=12, decimal_places=3)
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=30, default='SUBMITTED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.variation_number} - ₹{self.estimated_amount}"

class EOT(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eot_number = models.CharField(max_length=100, unique=True)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='eot_requests')
    file = models.ForeignKey('files.GovernmentFile', on_delete=models.SET_NULL, null=True, blank=True, related_name='eot_requests')
    original_completion_date = models.DateField()
    requested_completion_date = models.DateField()
    days_requested = models.IntegerField()
    reason = models.TextField()
    status = models.CharField(max_length=30, default='SUBMITTED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.eot_number} (+{self.days_requested} days)"

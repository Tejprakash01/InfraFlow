import uuid
from django.db import models

class DocumentCategory(models.TextChoices):
    CONTRACT = 'CONTRACT', 'Contract Document'
    DRAWING = 'DRAWING', 'Engineering Drawing'
    DPR = 'DPR', 'Daily Progress Report'
    WORK_PROGRAMME = 'WORK_PROGRAMME', 'Work Programme'
    INSPECTION = 'INSPECTION', 'Inspection Report'
    TEST_REPORT = 'TEST_REPORT', 'Quality Test Report'
    BILL = 'BILL', 'Bill Attachment'
    MEASUREMENT = 'MEASUREMENT', 'Measurement Sheet'
    CORRESPONDENCE = 'CORRESPONDENCE', 'Official Correspondence'
    APPROVAL = 'APPROVAL', 'Sanction / Approval Order'
    VARIATION = 'VARIATION', 'Variation Document'
    EOT = 'EOT', 'Extension of Time'
    COMPLETION = 'COMPLETION', 'Completion Certificate'

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='documents')
    file = models.ForeignKey('files.GovernmentFile', on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=30, choices=DocumentCategory.choices, default=DocumentCategory.CORRESPONDENCE)
    uploader = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    current_version_number = models.IntegerField(default=1)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (v{self.current_version_number})"

class DocumentVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='versions')
    version_number = models.IntegerField()
    file_attachment = models.FileField(upload_to='documents/%Y/%m/')
    file_size = models.BigIntegerField(default=0)
    comments = models.TextField(blank=True, default='')
    uploader = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('document', 'version_number')

    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"

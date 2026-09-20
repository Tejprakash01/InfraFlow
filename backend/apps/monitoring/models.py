import uuid
from django.db import models

class ReportTypeChoices(models.TextChoices):
    DAILY = 'DAILY', 'Daily Progress Report'
    WEEKLY = 'WEEKLY', 'Weekly Progress Report'
    MONTHLY = 'MONTHLY', 'Monthly Progress Report'

class ProgressReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='progress_reports')
    report_type = models.CharField(max_length=20, choices=ReportTypeChoices.choices, default=ReportTypeChoices.DAILY)
    report_date = models.DateField()
    physical_progress_pct = models.DecimalField(max_digits=5, decimal_places=2)
    financial_progress_pct = models.DecimalField(max_digits=5, decimal_places=2)
    manpower_count = models.IntegerField(default=0)
    equipment_count = models.IntegerField(default=0)
    work_executed_details = models.TextField()
    issues_encountered = models.TextField(blank=True, default='')
    reporter = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-report_date']

    def __str__(self):
        return f"{self.project.project_code} - {self.report_type} ({self.report_date})"

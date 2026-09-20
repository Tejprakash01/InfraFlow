from django.contrib import admin
from .models import ProgressReport

@admin.register(ProgressReport)
class ProgressReportAdmin(admin.ModelAdmin):
    list_display = ('project', 'report_type', 'report_date', 'physical_progress_pct', 'financial_progress_pct', 'reporter')

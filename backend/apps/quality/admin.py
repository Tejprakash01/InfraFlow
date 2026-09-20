from django.contrib import admin
from .models import SiteInspection, RFI, NCR, Variation, EOT

@admin.register(SiteInspection)
class SiteInspectionAdmin(admin.ModelAdmin):
    list_display = ('project', 'inspection_date', 'inspector', 'result')

@admin.register(RFI)
class RFIAdmin(admin.ModelAdmin):
    list_display = ('rfi_number', 'project', 'location', 'status')

@admin.register(NCR)
class NCRAdmin(admin.ModelAdmin):
    list_display = ('ncr_number', 'project', 'severity', 'status', 'due_date')

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('variation_number', 'project', 'estimated_amount', 'status')

@admin.register(EOT)
class EOTAdmin(admin.ModelAdmin):
    list_display = ('eot_number', 'project', 'days_requested', 'status')

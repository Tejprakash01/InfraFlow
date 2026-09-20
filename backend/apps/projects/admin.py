from django.contrib import admin
from .models import Project, Contract, ProjectMember, Milestone, WorkPackage, BOQItem

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_code', 'name', 'authority', 'regional_office', 'piu', 'contractor_org', 'status', 'physical_progress_pct')
    list_filter = ('status', 'authority', 'regional_office', 'piu')
    search_fields = ('project_code', 'name', 'location')

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'project', 'agreement_date', 'contract_value')

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'role_in_project', 'is_active')

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'target_date', 'is_achieved')

@admin.register(WorkPackage)
class WorkPackageAdmin(admin.ModelAdmin):
    list_display = ('project', 'name', 'planned_progress_pct', 'actual_progress_pct')

@admin.register(BOQItem)
class BOQItemAdmin(admin.ModelAdmin):
    list_display = ('project', 'item_code', 'description', 'unit', 'rate', 'sanctioned_quantity', 'executed_quantity')

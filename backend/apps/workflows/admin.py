from django.contrib import admin
from .models import WorkflowDefinition, WorkflowStep, WorkflowTransition, WorkflowInstance, WorkflowAction, SLAPolicy

@admin.register(WorkflowDefinition)
class WorkflowDefinitionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'is_active')

@admin.register(WorkflowStep)
class WorkflowStepAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'step_order', 'name', 'required_role', 'sla_hours')

@admin.register(WorkflowTransition)
class WorkflowTransitionAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'from_step', 'to_step', 'action_name')

@admin.register(WorkflowInstance)
class WorkflowInstanceAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'file', 'current_step', 'status', 'started_at')

@admin.register(SLAPolicy)
class SLAPolicyAdmin(admin.ModelAdmin):
    list_display = ('name', 'warning_threshold_hours', 'escalation_threshold_hours')

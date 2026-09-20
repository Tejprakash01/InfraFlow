import uuid
from django.db import models

class WorkflowDefinition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class WorkflowStep(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE, related_name='steps')
    step_order = models.IntegerField()
    name = models.CharField(max_length=150)
    required_role = models.CharField(max_length=50, blank=True, default='')
    sla_hours = models.IntegerField(default=48)
    approval_limit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    is_parallel = models.BooleanField(default=False)

    class Meta:
        ordering = ['step_order']
        unique_together = ('workflow', 'step_order')

    def __str__(self):
        return f"{self.workflow.code} - Step {self.step_order}: {self.name}"

class WorkflowTransition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE, related_name='transitions')
    from_step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE, related_name='outgoing_transitions')
    to_step = models.ForeignKey(WorkflowStep, on_delete=models.CASCADE, related_name='incoming_transitions')
    action_name = models.CharField(max_length=100)
    condition_expression = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.workflow.code}: {self.from_step.name} -> {self.to_step.name} on '{self.action_name}'"

class WorkflowInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.RESTRICT)
    file = models.OneToOneField('files.GovernmentFile', on_delete=models.CASCADE, related_name='workflow_instance')
    current_step = models.ForeignKey(WorkflowStep, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=30, default='ACTIVE')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Workflow {self.workflow.code} on {self.file.file_number} ({self.status})"

class WorkflowAction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instance = models.ForeignKey(WorkflowInstance, on_delete=models.CASCADE, related_name='actions')
    step = models.ForeignKey(WorkflowStep, on_delete=models.SET_NULL, null=True)
    actor = models.ForeignKey('accounts.User', on_delete=models.RESTRICT)
    action = models.CharField(max_length=100)
    remarks = models.TextField(blank=True, default='')
    timestamp = models.DateTimeField(auto_now_add=True)

class SLAPolicy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    warning_threshold_hours = models.IntegerField(default=24)
    escalation_threshold_hours = models.IntegerField(default=48)
    escalation_target_role = models.CharField(max_length=50, default='REGIONAL_OFFICER')

    def __str__(self):
        return self.name

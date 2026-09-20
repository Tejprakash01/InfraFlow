import uuid
from django.db import models

class ProjectStatus(models.TextChoices):
    PLANNING = 'PLANNING', 'Planning Phase'
    ACTIVE = 'ACTIVE', 'Active Execution'
    AT_RISK = 'AT_RISK', 'At Risk / Slow Progress'
    DELAYED = 'DELAYED', 'Delayed'
    COMPLETED = 'COMPLETED', 'Completed'
    CLOSED = 'CLOSED', 'Closed & Archived'

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    location = models.CharField(max_length=255)
    
    authority = models.ForeignKey('organizations.OrganizationNode', on_delete=models.RESTRICT, related_name='authority_projects')
    regional_office = models.ForeignKey('organizations.OrganizationNode', on_delete=models.SET_NULL, null=True, blank=True, related_name='regional_projects')
    piu = models.ForeignKey('organizations.OrganizationNode', on_delete=models.SET_NULL, null=True, blank=True, related_name='piu_projects')
    
    contractor_org = models.ForeignKey('organizations.OrganizationNode', on_delete=models.SET_NULL, null=True, blank=True, related_name='contractor_projects')
    consultant_org = models.ForeignKey('organizations.OrganizationNode', on_delete=models.SET_NULL, null=True, blank=True, related_name='consultant_projects')
    
    estimated_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    sanctioned_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    contract_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    
    start_date = models.DateField()
    scheduled_completion_date = models.DateField()
    actual_completion_date = models.DateField(null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.ACTIVE)
    
    physical_progress_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    financial_progress_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project_code} - {self.name}"

class Contract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='contract')
    contract_number = models.CharField(max_length=100, unique=True)
    letter_of_award_ref = models.CharField(max_length=100, blank=True, default='')
    agreement_date = models.DateField()
    work_order_date = models.DateField()
    contract_value = models.DecimalField(max_digits=15, decimal_places=2)
    defect_liability_period_months = models.IntegerField(default=24)
    performance_security_details = models.TextField(blank=True, default='')

    def __str__(self):
        return f"Contract {self.contract_number} ({self.project.name})"

class ProjectMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='project_assignments')
    role_in_project = models.CharField(max_length=50)
    assigned_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('project', 'user', 'role_in_project')

    def __str__(self):
        return f"{self.user.username} as {self.role_in_project} on {self.project.project_code}"

class Milestone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    name = models.CharField(max_length=255)
    target_date = models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    weightage_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_achieved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.project.project_code} - {self.name}"

class WorkPackage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='work_packages')
    name = models.CharField(max_length=255)
    planned_progress_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    actual_progress_pct = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.project.project_code} - {self.name}"

class BOQItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='boq_items')
    item_code = models.CharField(max_length=50)
    description = models.TextField()
    unit = models.CharField(max_length=20)
    rate = models.DecimalField(max_digits=12, decimal_places=2)
    sanctioned_quantity = models.DecimalField(max_digits=12, decimal_places=3)
    executed_quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0.000)

    class Meta:
        unique_together = ('project', 'item_code')

    def __str__(self):
        return f"{self.item_code}: {self.description[:40]}"

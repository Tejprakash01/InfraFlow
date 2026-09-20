import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class RoleChoices(models.TextChoices):
    HQ_ADMIN = 'HQ_ADMIN', 'HQ Administrator'
    REGIONAL_OFFICER = 'REGIONAL_OFFICER', 'Regional Officer'
    PROJECT_DIRECTOR = 'PROJECT_DIRECTOR', 'Project Director'
    AUTHORITY_ENGINEER = 'AUTHORITY_ENGINEER', 'Authority / Executive Engineer'
    SITE_ENGINEER = 'SITE_ENGINEER', 'Government Site Engineer'
    FINANCE_OFFICER = 'FINANCE_OFFICER', 'Finance / Accounts Officer'
    QUALITY_OFFICER = 'QUALITY_OFFICER', 'Quality Officer'
    CONSULTANT = 'CONSULTANT', 'Consultant'
    INDEPENDENT_ENGINEER = 'INDEPENDENT_ENGINEER', 'Independent Engineer'
    CONTRACTOR_ADMIN = 'CONTRACTOR_ADMIN', 'Contractor Administrator'
    CONTRACTOR_PROJECT_MANAGER = 'CONTRACTOR_PROJECT_MANAGER', 'Contractor Project Manager'
    CONTRACTOR_SITE_ENGINEER = 'CONTRACTOR_SITE_ENGINEER', 'Contractor Site Engineer'
    CONTRACTOR_PLANNING_ENGINEER = 'CONTRACTOR_PLANNING_ENGINEER', 'Contractor Planning Engineer'
    CONTRACTOR_BILLING_ENGINEER = 'CONTRACTOR_BILLING_ENGINEER', 'Contractor Billing Engineer'
    CONTRACTOR_QA_ENGINEER = 'CONTRACTOR_QA_ENGINEER', 'Contractor QA/QC Engineer'
    SUPER_ADMIN = 'SUPER_ADMIN', 'System Super Admin'

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    designation_title = models.CharField(max_length=100, blank=True, default='')
    role = models.CharField(max_length=40, choices=RoleChoices.choices, default=RoleChoices.PROJECT_DIRECTOR)
    organization = models.ForeignKey('organizations.OrganizationNode', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    department = models.ForeignKey('organizations.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    office = models.ForeignKey('organizations.Office', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    is_active_employee = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_government_user(self):
        return self.role in [
            RoleChoices.HQ_ADMIN, RoleChoices.REGIONAL_OFFICER,
            RoleChoices.PROJECT_DIRECTOR, RoleChoices.AUTHORITY_ENGINEER,
            RoleChoices.SITE_ENGINEER, RoleChoices.FINANCE_OFFICER,
            RoleChoices.QUALITY_OFFICER, RoleChoices.SUPER_ADMIN
        ]

    @property
    def is_contractor_user(self):
        return self.role.startswith('CONTRACTOR_')

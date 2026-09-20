import uuid
from django.db import models

class NodeTypeChoices(models.TextChoices):
    AUTHORITY = 'AUTHORITY', 'Government Authority'
    HQ = 'HQ', 'Headquarters'
    REGIONAL_OFFICE = 'REGIONAL_OFFICE', 'Regional Office'
    PIU = 'PIU', 'Project Implementation Unit / Division'
    CONTRACTOR = 'CONTRACTOR', 'Contractor Organization'
    CONSULTANT = 'CONSULTANT', 'Consultant Organization'

class OrganizationNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    node_type = models.CharField(max_length=30, choices=NodeTypeChoices.choices, default=NodeTypeChoices.AUTHORITY)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_node_type_display()})"

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(OrganizationNode, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)

    class Meta:
        unique_together = ('organization', 'code')

    def __str__(self):
        return f"{self.organization.name} - {self.name}"

class Office(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organization = models.ForeignKey(OrganizationNode, on_delete=models.CASCADE, related_name='offices')
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)
    location = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.organization.name} - {self.name}"

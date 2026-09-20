from django.contrib import admin
from .models import OrganizationNode, Department, Office

@admin.register(OrganizationNode)
class OrganizationNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'node_type', 'parent', 'is_active')
    list_filter = ('node_type', 'is_active')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'organization')

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'organization', 'location')

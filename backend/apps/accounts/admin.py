from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'designation_title', 'organization', 'is_active_employee')
    list_filter = ('role', 'is_active_employee', 'organization')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('InfraFlow Custom Fields', {
            'fields': ('role', 'designation_title', 'phone', 'organization', 'department', 'office', 'is_active_employee')
        }),
    )

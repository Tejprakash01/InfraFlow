from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'actor', 'action', 'entity_type', 'entity_id')
    readonly_fields = ('actor', 'organization', 'action', 'entity_type', 'entity_id', 'old_data', 'new_data', 'ip_address', 'user_agent', 'timestamp')

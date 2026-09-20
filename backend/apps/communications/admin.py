from django.contrib import admin
from .models import Correspondence, ProjectCommunication

@admin.register(Correspondence)
class CorrespondenceAdmin(admin.ModelAdmin):
    list_display = ('correspondence_number', 'subject', 'sender', 'recipient', 'status', 'due_date')

@admin.register(ProjectCommunication)
class ProjectCommunicationAdmin(admin.ModelAdmin):
    list_display = ('project', 'subject', 'sender', 'created_at')

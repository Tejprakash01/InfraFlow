from django.contrib import admin
from .models import GovernmentFile, FileNote, FileMovement, FileParticipant, FileDecision

@admin.register(GovernmentFile)
class GovernmentFileAdmin(admin.ModelAdmin):
    list_display = ('file_number', 'subject', 'project', 'current_holder', 'status', 'priority', 'is_overdue')
    list_filter = ('status', 'priority', 'confidentiality', 'is_overdue')
    search_fields = ('file_number', 'subject')

@admin.register(FileNote)
class FileNoteAdmin(admin.ModelAdmin):
    list_display = ('file', 'note_number', 'author', 'recommendation', 'is_finalized', 'created_at')

@admin.register(FileMovement)
class FileMovementAdmin(admin.ModelAdmin):
    list_display = ('file', 'from_user', 'to_user', 'action', 'timestamp')

@admin.register(FileDecision)
class FileDecisionAdmin(admin.ModelAdmin):
    list_display = ('file', 'decision_type', 'decision_by', 'timestamp')

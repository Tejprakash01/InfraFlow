from django.contrib import admin
from .models import Document, DocumentVersion

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'project', 'uploader', 'current_version_number', 'is_approved')

@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ('document', 'version_number', 'file_size', 'uploader', 'uploaded_at')

from rest_framework import serializers
from .models import Document, DocumentVersion

class DocumentVersionSerializer(serializers.ModelSerializer):
    uploader_name = serializers.CharField(source='uploader.get_full_name', read_only=True)

    class Meta:
        model = DocumentVersion
        fields = ['id', 'document', 'version_number', 'file_attachment', 'file_size', 'comments', 'uploader', 'uploader_name', 'uploaded_at']

class DocumentSerializer(serializers.ModelSerializer):
    uploader_name = serializers.CharField(source='uploader.get_full_name', read_only=True)
    versions = DocumentVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'project', 'file', 'title', 'category', 'uploader', 'uploader_name', 'current_version_number', 'is_approved', 'versions', 'created_at']
        read_only_fields = ['uploader']

from rest_framework import viewsets, permissions
from .models import Document, DocumentVersion
from .serializers import DocumentSerializer, DocumentVersionSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'HQ_ADMIN':
            return Document.objects.all()
        elif user.is_contractor_user and user.organization:
            return Document.objects.filter(project__contractor_org=user.organization)
        elif user.organization:
            return Document.objects.filter(project__piu=user.organization) | Document.objects.filter(project__authority=user.organization)
        return Document.objects.filter(uploader=user)

    def perform_create(self, serializer):
        doc = serializer.save(uploader=self.request.user)
        # If a file was attached in multipart form data
        file_obj = self.request.FILES.get('file') or self.request.FILES.get('file_attachment')
        if file_obj:
            DocumentVersion.objects.create(
                document=doc,
                version_number=1,
                file_attachment=file_obj,
                file_size=file_obj.size,
                comments=self.request.data.get('comments', 'Initial upload'),
                uploader=self.request.user
            )

class DocumentVersionViewSet(viewsets.ModelViewSet):
    queryset = DocumentVersion.objects.all()
    serializer_class = DocumentVersionSerializer
    permission_classes = [permissions.IsAuthenticated]

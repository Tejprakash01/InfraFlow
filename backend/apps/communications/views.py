from rest_framework import viewsets, permissions
from .models import Correspondence, ProjectCommunication
from .serializers import CorrespondenceSerializer, ProjectCommunicationSerializer

class CorrespondenceViewSet(viewsets.ModelViewSet):
    serializer_class = CorrespondenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'HQ_ADMIN':
            return Correspondence.objects.all()
        return Correspondence.objects.filter(sender=user) | Correspondence.objects.filter(recipient=user)

class ProjectCommunicationViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectCommunicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return ProjectCommunication.objects.filter(project__members__user=user) | ProjectCommunication.objects.filter(sender=user)

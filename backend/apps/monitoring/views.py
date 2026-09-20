from rest_framework import viewsets, permissions
from .models import ProgressReport
from .serializers import ProgressReportSerializer

class ProgressReportViewSet(viewsets.ModelViewSet):
    serializer_class = ProgressReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'HQ_ADMIN':
            return ProgressReport.objects.all()
        elif user.is_contractor_user and user.organization:
            return ProgressReport.objects.filter(project__contractor_org=user.organization)
        elif user.organization:
            return ProgressReport.objects.filter(project__piu=user.organization) | ProgressReport.objects.filter(project__authority=user.organization)
        return ProgressReport.objects.filter(reporter=user)

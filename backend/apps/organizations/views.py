from rest_framework import viewsets, permissions
from .models import OrganizationNode, Department, Office
from .serializers import OrganizationNodeSerializer, DepartmentSerializer, OfficeSerializer

class OrganizationNodeViewSet(viewsets.ModelViewSet):
    queryset = OrganizationNode.objects.all()
    serializer_class = OrganizationNodeSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class OfficeViewSet(viewsets.ModelViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework import viewsets, permissions
from .models import Project, Contract, ProjectMember, Milestone, WorkPackage, BOQItem
from .serializers import (
    ProjectSerializer, ContractSerializer, ProjectMemberSerializer,
    MilestoneSerializer, WorkPackageSerializer, BOQItemSerializer
)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'HQ_ADMIN':
            return Project.objects.all()
        elif user.role == 'REGIONAL_OFFICER' and user.organization:
            return Project.objects.filter(regional_office=user.organization)
        elif user.is_contractor_user and user.organization:
            return Project.objects.filter(contractor_org=user.organization)
        elif user.organization:
            return Project.objects.filter(piu=user.organization) | Project.objects.filter(authority=user.organization)
        return Project.objects.filter(members__user=user)

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkPackageViewSet(viewsets.ModelViewSet):
    queryset = WorkPackage.objects.all()
    serializer_class = WorkPackageSerializer
    permission_classes = [permissions.IsAuthenticated]

class BOQItemViewSet(viewsets.ModelViewSet):
    queryset = BOQItem.objects.all()
    serializer_class = BOQItemSerializer
    permission_classes = [permissions.IsAuthenticated]

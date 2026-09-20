from rest_framework import viewsets, permissions
from .models import WorkflowDefinition, WorkflowStep, WorkflowTransition, WorkflowInstance, WorkflowAction, SLAPolicy
from .serializers import (
    WorkflowDefinitionSerializer, WorkflowStepSerializer, WorkflowTransitionSerializer,
    WorkflowInstanceSerializer, WorkflowActionSerializer, SLAPolicySerializer
)

class WorkflowDefinitionViewSet(viewsets.ModelViewSet):
    queryset = WorkflowDefinition.objects.all()
    serializer_class = WorkflowDefinitionSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkflowStepViewSet(viewsets.ModelViewSet):
    queryset = WorkflowStep.objects.all()
    serializer_class = WorkflowStepSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkflowTransitionViewSet(viewsets.ModelViewSet):
    queryset = WorkflowTransition.objects.all()
    serializer_class = WorkflowTransitionSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkflowInstanceViewSet(viewsets.ModelViewSet):
    queryset = WorkflowInstance.objects.all()
    serializer_class = WorkflowInstanceSerializer
    permission_classes = [permissions.IsAuthenticated]

class SLAPolicyViewSet(viewsets.ModelViewSet):
    queryset = SLAPolicy.objects.all()
    serializer_class = SLAPolicySerializer
    permission_classes = [permissions.IsAuthenticated]

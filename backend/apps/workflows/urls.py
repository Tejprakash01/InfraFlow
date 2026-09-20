from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    WorkflowDefinitionViewSet, WorkflowStepViewSet, WorkflowTransitionViewSet,
    WorkflowInstanceViewSet, SLAPolicyViewSet
)

router = DefaultRouter()
router.register('definitions', WorkflowDefinitionViewSet, basename='workflow-definition')
router.register('steps', WorkflowStepViewSet, basename='workflow-step')
router.register('transitions', WorkflowTransitionViewSet, basename='workflow-transition')
router.register('instances', WorkflowInstanceViewSet, basename='workflow-instance')
router.register('sla-policies', SLAPolicyViewSet, basename='sla-policy')

urlpatterns = [
    path('', include(router.urls)),
]

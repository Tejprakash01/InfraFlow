from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet, ContractViewSet, ProjectMemberViewSet,
    MilestoneViewSet, WorkPackageViewSet, BOQItemViewSet
)

router = DefaultRouter()
router.register('projects', ProjectViewSet, basename='project')
router.register('contracts', ContractViewSet, basename='contract')
router.register('members', ProjectMemberViewSet, basename='project-member')
router.register('milestones', MilestoneViewSet, basename='milestone')
router.register('work-packages', WorkPackageViewSet, basename='work-package')
router.register('boq-items', BOQItemViewSet, basename='boq-item')

urlpatterns = [
    path('', include(router.urls)),
]

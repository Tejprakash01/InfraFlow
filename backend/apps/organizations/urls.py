from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationNodeViewSet, DepartmentViewSet, OfficeViewSet

router = DefaultRouter()
router.register('nodes', OrganizationNodeViewSet, basename='org-node')
router.register('departments', DepartmentViewSet, basename='department')
router.register('offices', OfficeViewSet, basename='office')

urlpatterns = [
    path('', include(router.urls)),
]

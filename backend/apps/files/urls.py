from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GovernmentFileViewSet

router = DefaultRouter()
router.register('files', GovernmentFileViewSet, basename='government-file')

urlpatterns = [
    path('', include(router.urls)),
]

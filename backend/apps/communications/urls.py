from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CorrespondenceViewSet, ProjectCommunicationViewSet

router = DefaultRouter()
router.register('correspondence', CorrespondenceViewSet, basename='correspondence')
router.register('project-communications', ProjectCommunicationViewSet, basename='project-communication')

urlpatterns = [
    path('', include(router.urls)),
]

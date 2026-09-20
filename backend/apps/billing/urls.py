from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MeasurementViewSet, BillViewSet

router = DefaultRouter()
router.register('measurements', MeasurementViewSet, basename='measurement')
router.register('bills', BillViewSet, basename='bill')

urlpatterns = [
    path('', include(router.urls)),
]

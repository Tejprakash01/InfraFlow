from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SiteInspectionViewSet, RFIViewSet, NCRViewSet, VariationViewSet, EOTViewSet

router = DefaultRouter()
router.register('inspections', SiteInspectionViewSet, basename='inspection')
router.register('rfis', RFIViewSet, basename='rfi')
router.register('ncrs', NCRViewSet, basename='ncr')
router.register('variations', VariationViewSet, basename='variation')
router.register('eots', EOTViewSet, basename='eot')

urlpatterns = [
    path('', include(router.urls)),
]

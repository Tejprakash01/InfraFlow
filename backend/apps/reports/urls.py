from django.urls import path
from .views import ExecutiveDashboardView, ContractorDashboardView

urlpatterns = [
    path('dashboard/executive/', ExecutiveDashboardView.as_view(), name='executive-dashboard'),
    path('dashboard/contractor/', ContractorDashboardView.as_view(), name='contractor-dashboard'),
]

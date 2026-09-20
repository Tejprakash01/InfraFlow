from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.db import connection

def health_check(request):
    db_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        db_ok = False
        
    return JsonResponse({
        "status": "ok" if db_ok else "error",
        "database": "ok" if db_ok else "unreachable",
        "version": "1.0.0",
        "platform": "InfraFlow"
    }, status=200 if db_ok else 500)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # OpenAPI Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Health Check Endpoint
    path('api/v1/health/', health_check, name='health-check'),
    
    # API Endpoints
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/organizations/', include('apps.organizations.urls')),
    path('api/v1/projects/', include('apps.projects.urls')),
    path('api/v1/files/', include('apps.files.urls')),
    path('api/v1/workflows/', include('apps.workflows.urls')),
    path('api/v1/documents/', include('apps.documents.urls')),
    path('api/v1/communications/', include('apps.communications.urls')),
    path('api/v1/monitoring/', include('apps.monitoring.urls')),
    path('api/v1/quality/', include('apps.quality.urls')),
    path('api/v1/billing/', include('apps.billing.urls')),
    path('api/v1/payments/', include('apps.payments.urls')),
    path('api/v1/audit/', include('apps.audit.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

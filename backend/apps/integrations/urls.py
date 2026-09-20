from django.urls import path
from django.http import JsonResponse

def integration_status(request):
    return JsonResponse({
        "adapters": {
            "pfms": "MockPFMSPaymentGateway (Ready)",
            "eoffice": "MockEOfficeAdapter (Ready)",
            "eprocurement": "MockEProcurementAdapter (Ready)",
            "esign": "MockDigitalSignatureProvider (Ready)"
        }
    })

urlpatterns = [
    path('status/', integration_status, name='integration-status'),
]

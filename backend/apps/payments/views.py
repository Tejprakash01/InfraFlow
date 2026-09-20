from rest_framework import viewsets, permissions
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role in ['HQ_ADMIN', 'FINANCE_OFFICER']:
            return Payment.objects.all()
        elif user.is_contractor_user and user.organization:
            return Payment.objects.filter(bill__project__contractor_org=user.organization)
        return Payment.objects.filter(processed_by=user)

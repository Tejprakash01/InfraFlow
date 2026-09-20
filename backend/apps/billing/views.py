from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Measurement, Bill, BillItem, BillStatus
from .serializers import MeasurementSerializer, BillSerializer, BillItemSerializer
from apps.files.models import GovernmentFile, FileStatus

class MeasurementViewSet(viewsets.ModelViewSet):
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'HQ_ADMIN':
            return Measurement.objects.all()
        return Measurement.objects.filter(project__members__user=user) | Measurement.objects.filter(verifier=user)

class BillViewSet(viewsets.ModelViewSet):
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'HQ_ADMIN':
            return Bill.objects.all()
        elif user.is_contractor_user and user.organization:
            return Bill.objects.filter(project__contractor_org=user.organization)
        elif user.organization:
            return Bill.objects.filter(project__piu=user.organization) | Bill.objects.filter(project__authority=user.organization)
        return Bill.objects.filter(submitted_by=user)

    def perform_create(self, serializer):
        user = self.request.user
        bill_count = Bill.objects.count() + 1
        bill_number = f"RABILL-2026-{bill_count:04d}"
        
        with transaction.atomic():
            bill = serializer.save(submitted_by=user, bill_number=bill_number, status=BillStatus.SUBMITTED)
            
            # Automatically create/link a Government File for bill approval tracking
            govt_file = GovernmentFile.objects.create(
                file_number=f"FILE-BILL-{bill_count:04d}",
                subject=f"Sanction & Payment of RA Bill #{bill_number} for {bill.project.name}",
                project=bill.project,
                file_type='BILL_SANCTION',
                priority='HIGH',
                originator=user,
                current_holder=user,
                status=FileStatus.REGISTERED
            )
            bill.government_file = govt_file
            bill.save()

    @action(detail=True, methods=['post'])
    def advance_status(self, request, pk=None):
        bill = self.get_object()
        next_status = request.data.get('next_status')
        if not next_status:
            return Response({'error': 'next_status is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        bill.status = next_status
        bill.save()
        return Response(BillSerializer(bill).data)

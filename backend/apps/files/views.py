from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.utils import timezone
from .models import GovernmentFile, FileNote, FileMovement, FileDecision, FileStatus, RecommendationChoices, DecisionTypeChoices
from .serializers import (
    GovernmentFileSerializer, FileNoteSerializer, FileMovementSerializer,
    FileDecisionSerializer, ForwardFileSerializer, ApproveFileSerializer
)
from apps.accounts.models import User

class GovernmentFileViewSet(viewsets.ModelViewSet):
    serializer_class = GovernmentFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = GovernmentFile.objects.all()
        
        if user.is_superuser or user.role == 'HQ_ADMIN':
            return queryset
        elif user.is_contractor_user:
            # Contractor users only see files related to their project where file confidentiality is not RESTRICTED
            return queryset.filter(project__contractor_org=user.organization).exclude(confidentiality='RESTRICTED')
        
        # Government officers see files in their org/dept or files held by them
        return queryset.filter(current_holder=user) | queryset.filter(project__piu=user.organization) | queryset.filter(project__regional_office=user.organization)

    def perform_create(self, serializer):
        user = self.request.user
        # Generate auto file number if not provided
        file_count = GovernmentFile.objects.count() + 1
        file_number = f"FILE-2026-{file_count:05d}"
        serializer.save(originator=user, current_holder=user, file_number=file_number, status=FileStatus.REGISTERED)

    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        file_obj = self.get_object()
        user = request.user
        content = request.data.get('content', '')
        recommendation = request.data.get('recommendation', RecommendationChoices.NEUTRAL)
        
        if not content:
            return Response({'error': 'Note content cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        next_note_num = file_obj.notes.count() + 1
        note = FileNote.objects.create(
            file=file_obj,
            note_number=next_note_num,
            author=user,
            content=content,
            recommendation=recommendation,
            is_finalized=False
        )
        return Response(FileNoteSerializer(note).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def forward(self, request, pk=None):
        file_obj = self.get_object()
        serializer = ForwardFileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        to_user_id = serializer.validated_data['to_user_id']
        action_text = serializer.validated_data['action']
        remarks = serializer.validated_data['remarks']
        expected_action = serializer.validated_data['expected_action']
        note_content = serializer.validated_data.get('note_content', '')
        recommendation = serializer.validated_data.get('recommendation', RecommendationChoices.NEUTRAL)

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response({'error': 'Target recipient user not found'}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            # Add note if provided
            if note_content:
                next_note_num = file_obj.notes.count() + 1
                FileNote.objects.create(
                    file=file_obj,
                    note_number=next_note_num,
                    author=request.user,
                    content=note_content,
                    recommendation=recommendation,
                    is_finalized=True
                )
            
            # Finalize any unfinalized notes by author
            file_obj.notes.filter(author=request.user, is_finalized=False).update(is_finalized=True)
            
            # Record movement
            FileMovement.objects.create(
                file=file_obj,
                from_user=request.user,
                to_user=to_user,
                from_department=file_obj.current_department,
                to_department=to_user.department,
                action=action_text,
                remarks=remarks,
                expected_action=expected_action
            )
            
            # Update file holder and status
            file_obj.current_holder = to_user
            file_obj.current_department = to_user.department
            file_obj.status = FileStatus.FORWARDED
            file_obj.save()

            # Synchronize linked RA Bill status along the workflow chain
            if hasattr(file_obj, 'linked_bill') and file_obj.linked_bill:
                from apps.billing.models import BillStatus
                bill = file_obj.linked_bill
                if to_user.role == 'FINANCE_OFFICER':
                    bill.status = BillStatus.FINANCE_REVIEW
                elif to_user.role in ['PROJECT_DIRECTOR', 'REGIONAL_OFFICER']:
                    bill.status = BillStatus.AUTHORITY_APPROVAL
                elif to_user.is_contractor_user:
                    bill.status = BillStatus.RETURNED
                elif to_user.role == 'AUTHORITY_ENGINEER':
                    bill.status = BillStatus.TECHNICAL_VERIFICATION
                bill.save()

        return Response(GovernmentFileSerializer(file_obj).data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        file_obj = self.get_object()
        serializer = ApproveFileSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        remarks = serializer.validated_data['remarks']
        decision_type = serializer.validated_data.get('decision_type', DecisionTypeChoices.APPROVED)

        with transaction.atomic():
            FileDecision.objects.create(
                file=file_obj,
                decision_type=decision_type,
                decision_by=request.user,
                remarks=remarks
            )
            
            file_obj.status = FileStatus.APPROVED if decision_type == DecisionTypeChoices.APPROVED else FileStatus.REJECTED
            file_obj.save()

            # Advance linked RA Bill and disburse payment record upon approval
            if hasattr(file_obj, 'linked_bill') and file_obj.linked_bill:
                from apps.billing.models import BillStatus
                from apps.payments.models import Payment, PaymentStatus
                bill = file_obj.linked_bill
                if decision_type == DecisionTypeChoices.APPROVED:
                    bill.status = BillStatus.PAID
                    bill.save()

                    Payment.objects.get_or_create(
                        bill=bill,
                        defaults={
                            'payment_reference': f"PFMS-{bill.bill_number}",
                            'utr_number': f"UTR{bill.bill_number.replace('-', '')}",
                            'amount': bill.net_amount,
                            'payment_date': timezone.now().date(),
                            'payment_status': PaymentStatus.DISBURSED,
                            'processed_by': request.user,
                            'remarks': remarks
                        }
                    )
                else:
                    bill.status = BillStatus.REJECTED
                    bill.save()

        return Response(GovernmentFileSerializer(file_obj).data)

    @action(detail=False, methods=['get'])
    def work_desk(self, request):
        user = request.user
        held_files = GovernmentFile.objects.filter(current_holder=user)
        overdue_files = held_files.filter(is_overdue=True)
        high_priority = held_files.filter(priority__in=['HIGH', 'URGENT'])
        
        return Response({
            'awaiting_action_count': held_files.count(),
            'overdue_count': overdue_files.count(),
            'high_priority_count': high_priority.count(),
            'files': GovernmentFileSerializer(held_files[:20], many=True).data
        })

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Sum, Count, Avg
from apps.projects.models import Project
from apps.files.models import GovernmentFile
from apps.billing.models import Bill
from apps.quality.models import RFI, NCR, SiteInspection

class ExecutiveDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        projects = Project.objects.all()
        files = GovernmentFile.objects.all()
        bills = Bill.objects.all()
        
        if user.is_contractor_user and user.organization:
            projects = projects.filter(contractor_org=user.organization)
            files = files.filter(project__contractor_org=user.organization)
            bills = bills.filter(project__contractor_org=user.organization)
        elif user.role == 'REGIONAL_OFFICER' and user.organization:
            projects = projects.filter(regional_office=user.organization)
            files = files.filter(project__regional_office=user.organization)

        total_contract_value = projects.aggregate(Sum('contract_value'))['contract_value__sum'] or 0
        avg_physical_progress = projects.aggregate(Avg('physical_progress_pct'))['physical_progress_pct__avg'] or 0
        avg_financial_progress = projects.aggregate(Avg('financial_progress_pct'))['financial_progress_pct__avg'] or 0
        
        pending_files_count = files.exclude(status__in=['APPROVED', 'REJECTED', 'CLOSED', 'COMPLETED']).count()
        overdue_files_count = files.filter(is_overdue=True).count()
        pending_bills_count = bills.exclude(status__in=['PAID', 'REJECTED']).count()
        open_ncrs_count = NCR.objects.filter(status='OPEN').count()
        
        return Response({
            'total_projects': projects.count(),
            'total_contract_value': total_contract_value,
            'avg_physical_progress_pct': round(avg_physical_progress, 2),
            'avg_financial_progress_pct': round(avg_financial_progress, 2),
            'pending_files_count': pending_files_count,
            'overdue_files_count': overdue_files_count,
            'pending_bills_count': pending_bills_count,
            'open_ncrs_count': open_ncrs_count,
            'projects_summary': [
                {
                    'id': str(p.id),
                    'code': p.project_code,
                    'name': p.name,
                    'status': p.status,
                    'physical_progress_pct': float(p.physical_progress_pct),
                    'financial_progress_pct': float(p.financial_progress_pct),
                    'contract_value': float(p.contract_value)
                } for p in projects[:10]
            ]
        })

class ContractorDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        contractor_org = user.organization
        projects = Project.objects.filter(contractor_org=contractor_org) if contractor_org else Project.objects.all()
        
        bills = Bill.objects.filter(project__in=projects)
        rfis = RFI.objects.filter(project__in=projects)
        ncrs = NCR.objects.filter(project__in=projects)
        
        return Response({
            'assigned_projects_count': projects.count(),
            'total_bills_submitted': bills.count(),
            'bills_pending_payment': bills.filter(status__in=['SUBMITTED', 'VERIFICATION', 'CERTIFIED', 'AUTHORITY_APPROVAL']).count(),
            'paid_bills_count': bills.filter(status='PAID').count(),
            'pending_rfis_count': rfis.exclude(status='APPROVED').count(),
            'open_ncrs_count': ncrs.filter(status='OPEN').count(),
            'recent_bills': [
                {
                    'id': str(b.id),
                    'bill_number': b.bill_number,
                    'project_name': b.project.name,
                    'net_amount': float(b.net_amount),
                    'status': b.status,
                    'submitted_at': b.created_at
                } for b in bills[:5]
            ]
        })

import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.organizations.models import OrganizationNode, Department, Office, NodeTypeChoices
from apps.accounts.models import User, RoleChoices
from apps.projects.models import Project, Contract, ProjectMember, Milestone, WorkPackage, BOQItem, ProjectStatus
from apps.files.models import GovernmentFile, FileNote, FileMovement, FileDecision, FileStatus, FilePriority, RecommendationChoices, DecisionTypeChoices
from apps.workflows.models import WorkflowDefinition, WorkflowStep, WorkflowTransition, WorkflowInstance
from apps.billing.models import Measurement, Bill, BillItem, BillStatus
from apps.payments.models import Payment, PaymentStatus
from apps.quality.models import SiteInspection, RFI, NCR, Variation, EOT, RFIStatus, NCRStatus, NCRSeverity, InspectionResult
from apps.notifications.models import Notification
from apps.audit.models import AuditLog

class Command(BaseCommand):
    help = 'Seeds initial demo data for InfraFlow highway infrastructure scenario.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting InfraFlow demo data seeding...'))

        # 1. Organization Tree
        authority, _ = OrganizationNode.objects.get_or_create(
            code='NIA-DEMO',
            defaults={
                'name': 'National Infrastructure Authority — DEMO',
                'node_type': NodeTypeChoices.AUTHORITY
            }
        )

        ro, _ = OrganizationNode.objects.get_or_create(
            code='RO-GUJ-DEMO',
            defaults={
                'name': 'Gujarat Regional Office — DEMO',
                'node_type': NodeTypeChoices.REGIONAL_OFFICE,
                'parent': authority
            }
        )

        piu, _ = OrganizationNode.objects.get_or_create(
            code='PIU-AMD-DEMO',
            defaults={
                'name': 'Ahmedabad PIU — DEMO',
                'node_type': NodeTypeChoices.PIU,
                'parent': ro
            }
        )

        contractor_org, _ = OrganizationNode.objects.get_or_create(
            code='CONT-ABC-DEMO',
            defaults={
                'name': 'ABC Infrastructure Pvt. Ltd. — DEMO',
                'node_type': NodeTypeChoices.CONTRACTOR
            }
        )

        consultant_org, _ = OrganizationNode.objects.get_or_create(
            code='CONS-IEC-DEMO',
            defaults={
                'name': 'Independent Engineering Consultants — DEMO',
                'node_type': NodeTypeChoices.CONSULTANT
            }
        )

        # 2. Departments
        eng_dept, _ = Department.objects.get_or_create(
            organization=piu, code='ENG', defaults={'name': 'Engineering Section'}
        )
        fin_dept, _ = Department.objects.get_or_create(
            organization=piu, code='FIN', defaults={'name': 'Finance & Accounts Division'}
        )

        # 3. Users Creation
        password = 'DemoPass123!'
        
        users_data = [
            ('admin@infraflow.gov.in', 'admin', RoleChoices.SUPER_ADMIN, 'System Super Administrator', authority, None),
            ('hq.admin@demo.in', 'hq_admin', RoleChoices.HQ_ADMIN, 'HQ Admin', authority, None),
            ('regional.officer@demo.in', 'regional_officer', RoleChoices.REGIONAL_OFFICER, 'Regional Officer', ro, None),
            ('project.director@demo.in', 'project_director', RoleChoices.PROJECT_DIRECTOR, 'Project Director', piu, eng_dept),
            ('authority.engineer@demo.in', 'authority_engineer', RoleChoices.AUTHORITY_ENGINEER, 'Authority Engineer', piu, eng_dept),
            ('finance.officer@demo.in', 'finance_officer', RoleChoices.FINANCE_OFFICER, 'Finance Officer', piu, fin_dept),
            ('quality.officer@demo.in', 'quality_officer', RoleChoices.QUALITY_OFFICER, 'Quality Officer', piu, eng_dept),
            ('consultant@demo.in', 'consultant_tl', RoleChoices.CONSULTANT, 'Consultant Team Leader', consultant_org, None),
            ('contractor.admin@demo.in', 'contractor_admin', RoleChoices.CONTRACTOR_ADMIN, 'Contractor Admin', contractor_org, None),
            ('contractor.pm@demo.in', 'contractor_pm', RoleChoices.CONTRACTOR_PROJECT_MANAGER, 'Contractor Project Manager', contractor_org, None),
            ('contractor.engineer@demo.in', 'contractor_eng', RoleChoices.CONTRACTOR_SITE_ENGINEER, 'Contractor Site Engineer', contractor_org, None),
            ('contractor.billing@demo.in', 'contractor_billing', RoleChoices.CONTRACTOR_BILLING_ENGINEER, 'Contractor Billing Engineer', contractor_org, None),
        ]

        created_users = {}
        for email, username, role, desig, org, dept in users_data:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': username,
                    'role': role,
                    'designation_title': desig,
                    'organization': org,
                    'department': dept,
                    'first_name': desig.split()[0],
                    'last_name': 'DEMO'
                }
            )
            if role in [RoleChoices.SUPER_ADMIN, RoleChoices.HQ_ADMIN]:
                user.is_staff = True
                user.is_superuser = True
            if created or not user.check_password(password):
                user.set_password(password)
            user.save()
            created_users[role] = user

        # 4. Projects Seeding
        start_date = datetime.date(2026, 1, 1)
        completion_date = datetime.date(2027, 12, 31)

        project1, _ = Project.objects.get_or_create(
            project_code='PROJ-NH-2026-01',
            defaults={
                'name': 'Ahmedabad–XYZ 4-Lane Highway — DEMO',
                'description': 'Four-laning of 45 km stretch on NH-47 under Bharatmala Pariyojana — DEMO',
                'location': 'Ahmedabad, Gujarat',
                'authority': authority,
                'regional_office': ro,
                'piu': piu,
                'contractor_org': contractor_org,
                'consultant_org': consultant_org,
                'estimated_cost': 500000000.00,
                'sanctioned_cost': 480000000.00,
                'contract_value': 450000000.00,
                'start_date': start_date,
                'scheduled_completion_date': completion_date,
                'status': ProjectStatus.ACTIVE,
                'physical_progress_pct': 38.50,
                'financial_progress_pct': 32.00
            }
        )

        Contract.objects.get_or_create(
            project=project1,
            defaults={
                'contract_number': 'CONT-2026-NH47-001',
                'agreement_date': start_date,
                'work_order_date': start_date,
                'contract_value': 450000000.00,
                'defect_liability_period_months': 36
            }
        )

        # Work Packages
        wp1, _ = WorkPackage.objects.get_or_create(
            project=project1, name='Earthwork & Subgrade',
            defaults={'planned_progress_pct': 70.00, 'actual_progress_pct': 65.00, 'start_date': start_date, 'end_date': start_date + datetime.timedelta(days=180)}
        )
        wp2, _ = WorkPackage.objects.get_or_create(
            project=project1, name='Drainage & Culverts',
            defaults={'planned_progress_pct': 45.00, 'actual_progress_pct': 40.00, 'start_date': start_date, 'end_date': start_date + datetime.timedelta(days=240)}
        )
        wp3, _ = WorkPackage.objects.get_or_create(
            project=project1, name='Flexible Pavement Execution',
            defaults={'planned_progress_pct': 25.00, 'actual_progress_pct': 20.00, 'start_date': start_date + datetime.timedelta(days=120), 'end_date': completion_date}
        )

        # BOQ Items
        boq1, _ = BOQItem.objects.get_or_create(
            project=project1, item_code='BOQ-01',
            defaults={'description': 'Excavation for Roadway in Soil', 'unit': 'cum', 'rate': 450.00, 'sanctioned_quantity': 100000.00, 'executed_quantity': 65000.00}
        )
        boq2, _ = BOQItem.objects.get_or_create(
            project=project1, item_code='BOQ-02',
            defaults={'description': 'Granular Sub-Base (GSB) Construction', 'unit': 'cum', 'rate': 1850.00, 'sanctioned_quantity': 50000.00, 'executed_quantity': 22000.00}
        )
        boq3, _ = BOQItem.objects.get_or_create(
            project=project1, item_code='BOQ-03',
            defaults={'description': 'M-25 Reinforced Concrete for Culverts', 'unit': 'cum', 'rate': 8500.00, 'sanctioned_quantity': 15000.00, 'executed_quantity': 6000.00}
        )

        # 5. Government Files
        pd_user = created_users[RoleChoices.PROJECT_DIRECTOR]
        ae_user = created_users[RoleChoices.AUTHORITY_ENGINEER]
        pm_user = created_users[RoleChoices.CONTRACTOR_PROJECT_MANAGER]
        ro_user = created_users[RoleChoices.REGIONAL_OFFICER]

        file1, _ = GovernmentFile.objects.get_or_create(
            file_number='FILE-2026-00421',
            defaults={
                'subject': 'Approval of Revised Work Programme — DEMO',
                'project': project1,
                'file_type': 'WORK_PROGRAMME_APPROVAL',
                'priority': FilePriority.HIGH,
                'originator': pd_user,
                'current_holder': pd_user,
                'status': FileStatus.APPROVED
            }
        )

        FileNote.objects.get_or_create(
            file=file1, note_number=1,
            defaults={
                'author': pm_user,
                'content': 'Contractor has submitted revised work programme incorporating monsoon mitigation schedule.',
                'recommendation': RecommendationChoices.NEUTRAL,
                'is_finalized': True
            }
        )
        FileNote.objects.get_or_create(
            file=file1, note_number=2,
            defaults={
                'author': ae_user,
                'content': 'Examined delay analysis and revised equipment deployment chart. Recommend approval subject to monthly monitoring.',
                'recommendation': RecommendationChoices.RECOMMEND_APPROVAL,
                'is_finalized': True
            }
        )

        FileDecision.objects.get_or_create(
            file=file1,
            defaults={
                'decision_type': DecisionTypeChoices.APPROVED,
                'decision_by': pd_user,
                'remarks': 'Revised work programme approved as recommended by Authority Engineer.'
            }
        )

        # Intentionally OVERDUE File for Demo Escalation
        overdue_file, _ = GovernmentFile.objects.get_or_create(
            file_number='FILE-2026-00388',
            defaults={
                'subject': 'Environmental Clearance Compliance & Utility Shifting File — OVERDUE DEMO',
                'project': project1,
                'file_type': 'ENVIRONMENTAL_CLEARANCE',
                'priority': FilePriority.URGENT,
                'originator': ae_user,
                'current_holder': ro_user,
                'status': FileStatus.PENDING_APPROVAL,
                'due_date': timezone.now() - datetime.timedelta(days=4),
                'is_overdue': True
            }
        )

        # 6. RA Bills Seeding
        bill1, _ = Bill.objects.get_or_create(
            bill_number='RABILL-2026-0001',
            defaults={
                'project': project1,
                'bill_period_start': start_date,
                'bill_period_end': start_date + datetime.timedelta(days=90),
                'gross_amount': 65400000.00,
                'deductions_amount': 3270000.00,
                'net_amount': 62130000.00,
                'status': BillStatus.PAID,
                'submitted_by': created_users[RoleChoices.CONTRACTOR_BILLING_ENGINEER]
            }
        )

        Payment.objects.get_or_create(
            bill=bill1,
            defaults={
                'payment_reference': 'PAY-2026-001',
                'utr_number': 'PFMSUTR987456123',
                'amount': 62130000.00,
                'payment_date': start_date + datetime.timedelta(days=100),
                'payment_status': PaymentStatus.DISBURSED,
                'remarks': 'RA Bill 01 payment disbursed via Mock PFMS Adapter',
                'processed_by': created_users[RoleChoices.FINANCE_OFFICER]
            }
        )

        # Quality & RFI
        RFI.objects.get_or_create(
            rfi_number='RFI-2026-0012',
            defaults={
                'project': project1,
                'work_package': wp2,
                'location': 'Chainage 18+400 Box Culvert',
                'requested_date': timezone.now(),
                'description': 'Request for inspection of foundation rebar layout before concrete pour.',
                'status': RFIStatus.APPROVED,
                'created_by': pm_user
            }
        )

        NCR.objects.get_or_create(
            ncr_number='NCR-2026-0005',
            defaults={
                'project': project1,
                'location': 'Chainage 24+500 Subgrade Layer',
                'work_package': wp1,
                'description': 'Compaction test failed to meet 98% MDD requirement.',
                'specification_breached': 'MORT&H Section 305 Table 300-2',
                'severity': NCRSeverity.MAJOR,
                'corrective_action_required': 'Re-roll and re-compact 200m section and re-test.',
                'status': NCRStatus.OPEN,
                'due_date': datetime.date.today() + datetime.timedelta(days=7),
                'created_by': created_users[RoleChoices.QUALITY_OFFICER]
            }
        )

        # 7. Additional Projects (Expressway & Bridge)
        project2, _ = Project.objects.get_or_create(
            project_code='PROJ-EX-2026-02',
            defaults={
                'name': 'Vadodara–Mumbai Expressway Package-4 — DEMO',
                'description': 'Construction of 8-lane Access-Controlled Expressway km 120.000 to km 158.000',
                'location': 'Surat, Gujarat',
                'authority': authority,
                'regional_office': ro,
                'piu': piu,
                'contractor_org': contractor_org,
                'consultant_org': consultant_org,
                'estimated_cost': 1200000000.00,
                'sanctioned_cost': 1150000000.00,
                'contract_value': 1080000000.00,
                'start_date': start_date + datetime.timedelta(days=30),
                'scheduled_completion_date': completion_date + datetime.timedelta(days=180),
                'status': ProjectStatus.ACTIVE,
                'physical_progress_pct': 52.00,
                'financial_progress_pct': 48.00
            }
        )

        project3, _ = Project.objects.get_or_create(
            project_code='PROJ-BR-2026-03',
            defaults={
                'name': 'Narmada River Cable-Stayed Bridge — DEMO',
                'description': 'Iconic 1.2 km 6-lane Extra-Dosed Cable Stayed Bridge across Narmada River',
                'location': 'Bharuch, Gujarat',
                'authority': authority,
                'regional_office': ro,
                'piu': piu,
                'contractor_org': contractor_org,
                'consultant_org': consultant_org,
                'estimated_cost': 750000000.00,
                'sanctioned_cost': 720000000.00,
                'contract_value': 690000000.00,
                'start_date': start_date - datetime.timedelta(days=120),
                'scheduled_completion_date': completion_date,
                'status': ProjectStatus.ACTIVE,
                'physical_progress_pct': 82.50,
                'financial_progress_pct': 78.00
            }
        )

        # 8. Project Members
        for prj in [project1, project2, project3]:
            for u in [pd_user, ae_user, pm_user, created_users[RoleChoices.CONTRACTOR_BILLING_ENGINEER]]:
                ProjectMember.objects.get_or_create(
                    project=prj,
                    user=u,
                    defaults={'role_in_project': u.designation_title or u.role, 'is_active': True}
                )

        # 9. Documents
        from apps.documents.models import Document, DocumentCategory
        doc1, _ = Document.objects.get_or_create(
            title='Contract Agreement Volume I & Special Conditions',
            defaults={
                'project': project1,
                'file': file1,
                'category': DocumentCategory.CONTRACT,
                'uploader': pd_user,
                'current_version_number': 1,
                'is_approved': True
            }
        )

        doc2, _ = Document.objects.get_or_create(
            title='Approved Alignment Drawing & Plan Profile Sheet (km 0+000 to 45+000)',
            defaults={
                'project': project1,
                'file': file1,
                'category': DocumentCategory.DRAWING,
                'uploader': ae_user,
                'current_version_number': 2,
                'is_approved': True
            }
        )

        doc3, _ = Document.objects.get_or_create(
            title='Revised Monsoon Work Programme Baseline-V2',
            defaults={
                'project': project1,
                'file': file1,
                'category': DocumentCategory.WORK_PROGRAMME,
                'uploader': pm_user,
                'current_version_number': 1,
                'is_approved': True
            }
        )

        doc4, _ = Document.objects.get_or_create(
            title='Quality Assurance Plan & Mix Design Approval for M-40 Grade',
            defaults={
                'project': project1,
                'category': DocumentCategory.TEST_REPORT,
                'uploader': created_users[RoleChoices.QUALITY_OFFICER],
                'current_version_number': 1,
                'is_approved': True
            }
        )

        doc5, _ = Document.objects.get_or_create(
            title='RA Bill No. 01 Signed Measurement Sheets & MB Abstract',
            defaults={
                'project': project1,
                'category': DocumentCategory.MEASUREMENT,
                'uploader': created_users[RoleChoices.CONTRACTOR_BILLING_ENGINEER],
                'current_version_number': 1,
                'is_approved': True
            }
        )

        # 10. Workflows & SLA Policies
        from apps.workflows.models import SLAPolicy, WorkflowDefinition, WorkflowStep
        sla_standard, _ = SLAPolicy.objects.get_or_create(
            name='Standard 48-Hour Technical Review SLA',
            defaults={
                'warning_threshold_hours': 24,
                'escalation_threshold_hours': 48,
                'escalation_target_role': 'REGIONAL_OFFICER'
            }
        )
        sla_urgent, _ = SLAPolicy.objects.get_or_create(
            name='Emergency Bill Sanction SLA (24-Hour)',
            defaults={
                'warning_threshold_hours': 12,
                'escalation_threshold_hours': 24,
                'escalation_target_role': 'PROJECT_DIRECTOR'
            }
        )

        wf_bill, _ = WorkflowDefinition.objects.get_or_create(
            code='WF-RA-BILL',
            defaults={
                'name': '11-Step RA Bill Scrutiny & Sanction Flow',
                'description': 'Sequential multi-tier verification process for contractor running account bills.',
                'is_active': True
            }
        )
        WorkflowStep.objects.get_or_create(workflow=wf_bill, step_order=1, defaults={'name': 'Site Engineer Quantity Check', 'required_role': 'AUTHORITY_ENGINEER', 'sla_hours': 24})
        WorkflowStep.objects.get_or_create(workflow=wf_bill, step_order=2, defaults={'name': 'Quality Officer Testing Compliance', 'required_role': 'QUALITY_OFFICER', 'sla_hours': 24})
        WorkflowStep.objects.get_or_create(workflow=wf_bill, step_order=3, defaults={'name': 'Finance & Accounts Scrutiny', 'required_role': 'FINANCE_OFFICER', 'sla_hours': 48})
        WorkflowStep.objects.get_or_create(workflow=wf_bill, step_order=4, defaults={'name': 'Project Director Final Sanction', 'required_role': 'PROJECT_DIRECTOR', 'sla_hours': 24})

        wf_wp, _ = WorkflowDefinition.objects.get_or_create(
            code='WF-WORK-PROG',
            defaults={
                'name': 'Work Programme Revision & Delay Mitigation Approval',
                'description': 'Evaluation and approval of contractor revised resource charts and baseline schedules.',
                'is_active': True
            }
        )

        # 11. Additional RA Bill (Under Review)
        bill2, _ = Bill.objects.get_or_create(
            bill_number='RABILL-2026-0002',
            defaults={
                'project': project1,
                'bill_period_start': start_date + datetime.timedelta(days=91),
                'bill_period_end': start_date + datetime.timedelta(days=180),
                'gross_amount': 82500000.00,
                'deductions_amount': 4125000.00,
                'net_amount': 78375000.00,
                'status': BillStatus.TECHNICAL_VERIFICATION,
                'submitted_by': created_users[RoleChoices.CONTRACTOR_BILLING_ENGINEER]
            }
        )

        # 12. Audit Logs
        from apps.audit.models import AuditLog
        AuditLog.objects.get_or_create(
            action='BILL_SUBMISSION',
            entity_type='Bill',
            entity_id=str(bill2.id),
            defaults={
                'actor': created_users[RoleChoices.CONTRACTOR_BILLING_ENGINEER],
                'organization': contractor_org,
                'new_data': {'bill_number': bill2.bill_number, 'net_amount': 78375000.00},
                'ip_address': '10.200.19.199'
            }
        )
        AuditLog.objects.get_or_create(
            action='FILE_APPROVED',
            entity_type='GovernmentFile',
            entity_id=str(file1.id),
            defaults={
                'actor': pd_user,
                'organization': piu,
                'new_data': {'file_number': file1.file_number, 'status': 'APPROVED'},
                'ip_address': '10.200.19.199'
            }
        )

        # 13. System Notifications
        from apps.notifications.models import Notification
        for u in [pd_user, ae_user, pm_user, created_users[RoleChoices.HQ_ADMIN]]:
            Notification.objects.get_or_create(
                recipient=u,
                title='Welcome to InfraFlow Infrastructure Portal',
                defaults={
                    'message': f'Your account has been configured with role: {u.get_role_display()} on NH-47 Project.',
                    'link': '/projects',
                    'is_read': False
                }
            )
            Notification.objects.get_or_create(
                recipient=u,
                title='RA Bill #02 Submitted for Scrutiny',
                defaults={
                    'message': 'Contractor ABC Infrastructure Pvt. Ltd. has submitted RA Bill-0002 for ₹7.83 Cr.',
                    'link': '/bills',
                    'is_read': False
                }
            )

        self.stdout.write(self.style.SUCCESS('InfraFlow demo environment successfully seeded!'))

from rest_framework import serializers
from .models import Project, Contract, ProjectMember, Milestone, WorkPackage, BOQItem

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class ProjectMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    role_display = serializers.CharField(source='user.get_role_display', read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'project', 'user', 'username', 'full_name', 'role_display', 'role_in_project', 'assigned_at', 'is_active']

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = '__all__'

class WorkPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPackage
        fields = '__all__'

class BOQItemSerializer(serializers.ModelSerializer):
    sanctioned_amount = serializers.SerializerMethodField()
    executed_amount = serializers.SerializerMethodField()

    class Meta:
        model = BOQItem
        fields = ['id', 'project', 'item_code', 'description', 'unit', 'rate', 'sanctioned_quantity', 'executed_quantity', 'sanctioned_amount', 'executed_amount']

    def get_sanctioned_amount(self, obj):
        return obj.rate * obj.sanctioned_quantity

    def get_executed_amount(self, obj):
        return obj.rate * obj.executed_quantity

class ProjectSerializer(serializers.ModelSerializer):
    authority_name = serializers.CharField(source='authority.name', read_only=True)
    regional_office_name = serializers.CharField(source='regional_office.name', read_only=True)
    piu_name = serializers.CharField(source='piu.name', read_only=True)
    contractor_name = serializers.CharField(source='contractor_org.name', read_only=True)
    consultant_name = serializers.CharField(source='consultant_org.name', read_only=True)
    members = ProjectMemberSerializer(many=True, read_only=True)
    milestones = MilestoneSerializer(many=True, read_only=True)
    work_packages = WorkPackageSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id', 'project_code', 'name', 'description', 'location',
            'authority', 'authority_name', 'regional_office', 'regional_office_name',
            'piu', 'piu_name', 'contractor_org', 'contractor_name',
            'consultant_org', 'consultant_name', 'estimated_cost',
            'sanctioned_cost', 'contract_value', 'start_date',
            'scheduled_completion_date', 'actual_completion_date', 'status',
            'physical_progress_pct', 'financial_progress_pct', 'members',
            'milestones', 'work_packages', 'created_at'
        ]

from rest_framework import serializers
from .models import OrganizationNode, Department, Office

class OrganizationNodeSerializer(serializers.ModelSerializer):
    node_type_display = serializers.CharField(source='get_node_type_display', read_only=True)
    parent_name = serializers.CharField(source='parent.name', read_only=True)

    class Meta:
        model = OrganizationNode
        fields = ['id', 'name', 'code', 'node_type', 'node_type_display', 'parent', 'parent_name', 'is_active', 'created_at']

class DepartmentSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'organization', 'organization_name', 'name', 'code']

class OfficeSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)

    class Meta:
        model = Office
        fields = ['id', 'organization', 'organization_name', 'name', 'code', 'location']

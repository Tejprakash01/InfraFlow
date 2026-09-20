from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    department_name = serializers.CharField(source='department.name', read_only=True)
    office_name = serializers.CharField(source='office.name', read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'designation_title', 'role', 'role_display',
            'organization', 'organization_name', 'department',
            'department_name', 'office', 'office_name',
            'is_active_employee', 'is_government_user', 'is_contractor_user',
            'is_staff', 'is_superuser'
        ]
        read_only_fields = ['id']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

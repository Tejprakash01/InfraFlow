from rest_framework import serializers
from .models import GovernmentFile, FileNote, FileMovement, FileParticipant, FileDecision

class FileNoteSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    author_full_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_designation = serializers.CharField(source='author.designation_title', read_only=True)

    class Meta:
        model = FileNote
        fields = ['id', 'file', 'note_number', 'author', 'author_username', 'author_full_name', 'author_designation', 'content', 'recommendation', 'is_finalized', 'created_at']

class FileMovementSerializer(serializers.ModelSerializer):
    from_user_name = serializers.CharField(source='from_user.get_full_name', read_only=True)
    to_user_name = serializers.CharField(source='to_user.get_full_name', read_only=True)
    from_dept_name = serializers.CharField(source='from_department.name', read_only=True, default='')
    to_dept_name = serializers.CharField(source='to_department.name', read_only=True, default='')

    class Meta:
        model = FileMovement
        fields = ['id', 'file', 'from_user', 'from_user_name', 'to_user', 'to_user_name', 'from_department', 'from_dept_name', 'to_department', 'to_dept_name', 'action', 'remarks', 'expected_action', 'due_date', 'timestamp']

class FileDecisionSerializer(serializers.ModelSerializer):
    decision_by_name = serializers.CharField(source='decision_by.get_full_name', read_only=True)

    class Meta:
        model = FileDecision
        fields = ['id', 'file', 'decision_type', 'decision_by', 'decision_by_name', 'remarks', 'timestamp']

class GovernmentFileSerializer(serializers.ModelSerializer):
    project_code = serializers.CharField(source='project.project_code', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    originator_name = serializers.CharField(source='originator.get_full_name', read_only=True)
    current_holder_name = serializers.CharField(source='current_holder.get_full_name', read_only=True)
    current_holder_designation = serializers.CharField(source='current_holder.designation_title', read_only=True)
    notes = FileNoteSerializer(many=True, read_only=True)
    movements = FileMovementSerializer(many=True, read_only=True)
    decisions = FileDecisionSerializer(many=True, read_only=True)

    class Meta:
        model = GovernmentFile
        fields = [
            'id', 'file_number', 'subject', 'project', 'project_code',
            'project_name', 'department', 'office', 'file_type', 'priority',
            'confidentiality', 'originator', 'originator_name',
            'current_holder', 'current_holder_name', 'current_holder_designation',
            'current_department', 'status', 'due_date', 'is_overdue',
            'notes', 'movements', 'decisions', 'created_at', 'updated_at'
        ]

class ForwardFileSerializer(serializers.Serializer):
    to_user_id = serializers.UUIDField()
    action = serializers.CharField(default='FORWARD')
    remarks = serializers.CharField(required=False, allow_blank=True, default='')
    expected_action = serializers.CharField(required=False, allow_blank=True, default='')
    note_content = serializers.CharField(required=False, allow_blank=True, default='')
    recommendation = serializers.CharField(required=False, default='NEUTRAL')

class ApproveFileSerializer(serializers.Serializer):
    remarks = serializers.CharField()
    decision_type = serializers.CharField(default='APPROVED')

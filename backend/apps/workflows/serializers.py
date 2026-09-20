from rest_framework import serializers
from .models import WorkflowDefinition, WorkflowStep, WorkflowTransition, WorkflowInstance, WorkflowAction, SLAPolicy

class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowStep
        fields = '__all__'

class WorkflowTransitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowTransition
        fields = '__all__'

class WorkflowDefinitionSerializer(serializers.ModelSerializer):
    steps = WorkflowStepSerializer(many=True, read_only=True)
    transitions = WorkflowTransitionSerializer(many=True, read_only=True)

    class Meta:
        model = WorkflowDefinition
        fields = ['id', 'name', 'code', 'description', 'is_active', 'steps', 'transitions']

class WorkflowActionSerializer(serializers.ModelSerializer):
    actor_name = serializers.CharField(source='actor.get_full_name', read_only=True)

    class Meta:
        model = WorkflowAction
        fields = ['id', 'instance', 'step', 'actor', 'actor_name', 'action', 'remarks', 'timestamp']

class WorkflowInstanceSerializer(serializers.ModelSerializer):
    workflow_name = serializers.CharField(source='workflow.name', read_only=True)
    current_step_name = serializers.CharField(source='current_step.name', read_only=True)
    actions = WorkflowActionSerializer(many=True, read_only=True)

    class Meta:
        model = WorkflowInstance
        fields = ['id', 'workflow', 'workflow_name', 'file', 'current_step', 'current_step_name', 'status', 'actions', 'started_at', 'completed_at']

class SLAPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = SLAPolicy
        fields = '__all__'

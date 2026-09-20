from rest_framework import serializers
from .models import Correspondence, ProjectCommunication

class CorrespondenceSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)
    recipient_name = serializers.CharField(source='recipient.get_full_name', read_only=True)

    class Meta:
        model = Correspondence
        fields = '__all__'

class ProjectCommunicationSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.get_full_name', read_only=True)

    class Meta:
        model = ProjectCommunication
        fields = '__all__'

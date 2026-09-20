from rest_framework import serializers
from .models import ProgressReport

class ProgressReportSerializer(serializers.ModelSerializer):
    reporter_name = serializers.CharField(source='reporter.get_full_name', read_only=True)

    class Meta:
        model = ProgressReport
        fields = '__all__'

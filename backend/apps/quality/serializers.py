from rest_framework import serializers
from .models import SiteInspection, RFI, NCR, Variation, EOT

class SiteInspectionSerializer(serializers.ModelSerializer):
    inspector_name = serializers.CharField(source='inspector.get_full_name', read_only=True)

    class Meta:
        model = SiteInspection
        fields = '__all__'

class RFISerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = RFI
        fields = '__all__'
        read_only_fields = ['id', 'rfi_number', 'created_by', 'status', 'created_at']

class NCRSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = NCR
        fields = '__all__'
        read_only_fields = ['id', 'ncr_number', 'created_by', 'status', 'created_at']

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = '__all__'

class EOTSerializer(serializers.ModelSerializer):
    class Meta:
        model = EOT
        fields = '__all__'

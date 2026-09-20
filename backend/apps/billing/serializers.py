from rest_framework import serializers
from .models import Measurement, Bill, BillItem

class MeasurementSerializer(serializers.ModelSerializer):
    verifier_name = serializers.CharField(source='verifier.get_full_name', read_only=True)
    item_code = serializers.CharField(source='boq_item.item_code', read_only=True)

    class Meta:
        model = Measurement
        fields = '__all__'

class BillItemSerializer(serializers.ModelSerializer):
    item_code = serializers.CharField(source='boq_item.item_code', read_only=True)
    description = serializers.CharField(source='boq_item.description', read_only=True)
    unit = serializers.CharField(source='boq_item.unit', read_only=True)

    class Meta:
        model = BillItem
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    submitted_by_name = serializers.CharField(source='submitted_by.get_full_name', read_only=True)
    project_code = serializers.CharField(source='project.project_code', read_only=True)
    file_number = serializers.CharField(source='government_file.file_number', read_only=True, default='')
    items = BillItemSerializer(many=True, read_only=True)

    class Meta:
        model = Bill
        fields = [
            'id', 'bill_number', 'project', 'project_code', 'government_file', 'file_number',
            'bill_period_start', 'bill_period_end', 'gross_amount', 'deductions_amount',
            'net_amount', 'status', 'submitted_by', 'submitted_by_name', 'items', 'created_at'
        ]
        read_only_fields = ['id', 'bill_number', 'government_file', 'submitted_by', 'status', 'created_at']

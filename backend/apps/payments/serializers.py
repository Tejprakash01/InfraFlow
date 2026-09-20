from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    processed_by_name = serializers.CharField(source='processed_by.get_full_name', read_only=True)
    bill_number = serializers.CharField(source='bill.bill_number', read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'

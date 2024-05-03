from rest_framework import serializers
from po_tracking.models import PurchaseOrder


class POSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

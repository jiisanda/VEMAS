from rest_framework import serializers
from po_tracking.models import PurchaseOrder


class POSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.items = validated_data.get('items', instance.items)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.acknowledgment_date = validated_data.get('acknowledgment_date', instance.acknowledgment_date)
        instance.quality_rating = validated_data.get('quality_rating', instance.quality_rating)
        instance.save()
        return instance

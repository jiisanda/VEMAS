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


class POSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    def validate(self, attrs):
        if 'expected_delivery_date' not in attrs:
            raise serializers.ValidationError({"expected_delivery_date": "This field is required."})
        if 'quantity' not in attrs:
            raise serializers.ValidationError({"quantity": "This field is required."})
        if 'items' not in attrs:
            raise serializers.ValidationError({"items": "This field is required."})
        return attrs

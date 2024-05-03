from rest_framework import serializers
from vendor.models import Vendor, PerformanceHistory


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class PHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PerformanceHistory
        fields = '__all__'


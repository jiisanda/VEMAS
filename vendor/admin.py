from django.contrib import admin
from vendor.models import Vendor, PerformanceHistory


class VendorAdmin(admin.ModelAdmin):
    readonly_fields = ('on_time_delivery_rate', 'average_response_time', 'quality_rating_avg', 'fulfillment_rate')


# Register vendor models here
admin.site.register(Vendor, VendorAdmin)
admin.site.register(PerformanceHistory)

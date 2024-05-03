from django.contrib import admin
from vendor.models import Vendor, PerformanceHistory

# Register vendor models here
admin.site.register(Vendor)
admin.site.register(PerformanceHistory)

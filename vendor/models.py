import random
import string

from django.db import models
from django.utils import timezone


# Vendor model
class Vendor(models.Model):
    uvc = models.CharField(max_length=6, unique=True, editable=False, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(default=0.0, editable=False)
    quality_rating_avg = models.FloatField(default=0.0, editable=False)
    average_response_time = models.CharField(max_length=100, editable=False, blank=True)
    fulfillment_rate = models.FloatField(default=0.0, editable=False)

    def save(self, *args, **kwargs):
        if not self.uvc:
            # generating a random alphanumeric code of length 6 uvc - Unique Vendor code
            self.uvc = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.uvc} | {self.name}"


class PerformanceHistory(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField(default=timezone.now, blank=False)
    on_time_delivery_rate = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.vendor} | {self.date} - Performance"

    class Meta:
        ordering = ['-date']

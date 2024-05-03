import random
import string

from django.db import models
from django.utils import timezone

from vendor.models import Vendor


# Purchase Order Tracking model
class PurchaseOrder(models.Model):
    class StatusChoices(models.TextChoices):
        pending = 'pending'
        completed = 'completed'
        canceled = 'canceled'

    po_number = models.CharField(max_length=8, unique=True, editable=False, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=False)
    order_date = models.DateTimeField(default=timezone.now, blank=False)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.pending)
    quality_rating = models.FloatField(null=True)
    issue_data = models.DateTimeField(default=timezone.now, blank=False)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.po_number:
            # generating a random alphanumeric code of length 8 po_number - Purchase Order number
            self.po_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.po_number} | {self.vendor.name}"

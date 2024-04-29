import random
import string

from django.db import models


# Vendor model
class Vendor(models.Model):
    uvc = models.CharField(max_length=6, unique=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        if not self.uvc:
            # generating a random alphanumeric code of length 6 uvc - Unique Vendor code
            self.uvc = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.uvc} | {self.name}"

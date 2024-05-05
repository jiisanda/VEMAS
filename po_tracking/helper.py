from typing import Dict, Union

from django.db.models import F, Avg, Q

from po_tracking.models import PurchaseOrder
from vendor.models import PerformanceHistory, Vendor


def update_metrics(vendor: str) -> Dict[str, Union[float, str]]:
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

    # Step1: ans = calculate no of completed POs delivered on or before delivery_date
    on_time_pos = completed_pos.filter(Q(actual_delivery_date__lte=F('expected_delivery_date')) | Q(actual_delivery_date__isnull=True)).count()
    # Step2: ans = ans / total no of completed POs
    on_time_delivery_rate = (on_time_pos / completed_pos.count()) * 100 if completed_pos.count() else 0

    # Step1: Average of all quality_rating for completed POs
    quality_rating_avg = completed_pos.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']

    # step1: fulfillment rate = total pos with status 'completed' divided by total POs issued to vendor
    fulfillment_rate = (completed_pos.filter(quality_rating__gte=3).count() / PurchaseOrder.objects.filter(
        vendor=vendor).count()) * 100

    return {
        'on_time_delivery_rate': on_time_delivery_rate,
        'quality_rating_avg': quality_rating_avg,
        'fulfillment_rate': fulfillment_rate,
        'average_response_time': vendor.average_response_time
    }


def update_vendor_and_history(vendor: str, metrics: Dict[str, float]) -> None:
    # todo: @jiisanda: Error Handling here...
    vendor = Vendor.objects.get(uvc=vendor)

    vendor.on_time_delivery_rate = metrics['on_time_delivery_rate']
    vendor.quality_rating_avg = metrics['quality_rating_avg']
    vendor.fulfillment_rate = metrics['fulfillment_rate']
    vendor.average_response_time = metrics['average_response_time']

    vendor.save()

    # Update history
    PerformanceHistory(
        vendor=vendor,
        on_time_delivery_rate=metrics['on_time_delivery_rate'],
        quality_rating_avg=metrics['quality_rating_avg'],
        average_response_time=metrics['average_response_time'],
        fulfillment_rate=metrics['fulfillment_rate']
    ).save()

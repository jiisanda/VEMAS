# Performance Metrics Calculation

## Description

Performance Metrics gets calculated every time if purchase order status is updated to `completed' or the purchase order is acknowledged by the vendor. The performance metrics are calculated based on the following parameters:

- On Time Delivery Rate
- Quality Rating
- Average Response Time
- Fulfillment Rate

## On Time Delivery Rate

- Calculated each time a PO status changes to 'completed'.
- Logic: Count the number of completed POs delivered on or before
`delivery_date` and divide by the total number of completed POs for that vendor.

### Formula

```python
# Step1: ans = calculate no of completed POs delivered on or before delivery_date
on_time_pos = completed_pos.filter(Q(actual_delivery_date__lte=F('expected_delivery_date')) | Q(actual_delivery_date__isnull=True)).count()
# Step2: ans = ans / total no of completed POs
on_time_delivery_rate = (on_time_pos / completed_pos.count()) * 100 if completed_pos.count() else 0
```

## Quality Rating

- Updated upon the completion of each PO where a `quality_rating` is provided.
●- Logic: Calculate the average of all `quality_rating` values for completed POs of
the vendor.

### Formula

```python
# Step1: Average of all quality_rating for completed POs
quality_rating_avg = completed_pos.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']
``` 

## Average Response Time

- Calculated each time a PO is acknowledged by the vendor.
- Logic: Compute the time difference between `issue_date` and
`acknowledgment_date` for each PO, and then find the average of these times
for all POs of the vendor.

### Formula

```python
average_response_time = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).aggregate(
    avg_response_time=Avg(
        ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
    )
)['avg_response_time']
```

## Fulfillment Rate

- Calculated upon any change in PO status.
- Logic: Divide the number of successfully fulfilled POs (status `completed`
without issues) by the total number of POs issued to the vendor.

```python
# step1: fulfillment rate = total pos with status 'completed' divided by total POs issued to vendor
fulfillment_rate = (completed_pos.filter(quality_rating__gte=3).count() / PurchaseOrder.objects.filter(
    vendor=vendor).count()) * 100
```

[helper.py](../../po_tracking/helper.py) contains the helper functions for calculating the performance metrics.

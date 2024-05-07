# Purchase Order Management API

## Contents

- [Model Definition](#model-definitions)
- [API Endpoints](#api-endpoints)
  - [Create Purchase Order](#create-purchase-order)
  - [Get Purchase Orders](#get-purchase-orders)
  - [Get Purchase Order](#get-purchase-order)
  - [Update Purchase Order](#update-purchase-order)
  - [Delete Purchase Order](#delete-purchase-order)
  - [Acknowledge Purchase Order](#acknowledge-purchase-order)

## Model Definitions

```text
PurchaseOrder {
  po_number: string [unique] [required] [purchase order number]
  vendor: ForeignKey [required] [Vendor.uvc]
  order_date: DateTimeField [required] [order date]
  expected_delivery_date: DateTimeField [required] [expected delivery date]
  actual_delivery_date: DateTimeField [actual delivery date]
  items: JSONField [required] [items in the purchase order]
  quantity: int [required] [total amount of the purchase order]
  status: StatusChoices [pending, completed, canceled] [default=pending] [status of the purchase order]
  quality_rating: float [quality rating of the purchase order] [not editable]
  issue_date: string [required] [timestamp of the purchase order creation]
  acknowledgment_date: string [required] [timestamp of the purchase order getting acknowledged]
}
```

## API Endpoints

### Create Purchase Order

```http
POST /api/purchase_orders/
```

#### Request Body

```json
{
  "po_number": "string",
  "vendor": "string",
  "order_date": "string",
  "expected_delivery_date": "string",
  "items": "string",
  "quantity": "int",
  "status": "pending",
  "issue_date": "string"
}
```

`po_number` gets generated automatically and is a random alphanumeric string of length 6.

#### Response

```json
{
  "po_number": "string",
  "vendor": "string",
  "order_date": "string",
  "expected_delivery_date": "string",
  "actual_delivery_date": null,
  "items": "string",
  "quantity": "int",
  "status": "pending",
  "quality_rating": 0.0,
  "issue_date": "string",
  "acknowledgment_date": null
}
```

### Get Purchase Orders

```http
GET /api/purchase_orders/
```

#### Response

```json
[
  {
    "po_number": "string", 
    "vendor": "string",
    "order_date": "string",
    "expected_delivery_date": "string",
    "actual_delivery_date": "string",
    "items": "string",
    "quantity": "int",
    "status": "pending",
    "quality_rating": 0.0,
    "issue_date": "string",
    "acknowledgment_date": "string"
  }
]
```


### Get Purchase Order

```http
GET /api/purchase_orders/{po_number}/
```

#### Response

```json
{
  "po_number": "string",
  "vendor": "string",
  "order_date": "string",
  "expected_delivery_date": "string",
  "actual_delivery_date": "string",
  "items": "string",
  "quantity": "int",
  "status": "pending",
  "quality_rating": 0.0,
  "issue_date": "string",
  "acknowledgment_date": "string"
}
```

### Update Purchase Order

```http
PUT /api/purchase_orders/{po_number}/
```

#### Request Body

```json
{
  "status": "string",
  "quality_rating": "float",
  "actual_delivery_date": "string"
}
```

#### Response 

```json
{
  "po_number": "string",
  "vendor": "string",
  "order_date": "string",
  "expected_delivery_date": "string",
  "actual_delivery_date": "string",
  "items": "string",
  "quantity": "int",
  "status": "pending",
  "quality_rating": 0.0,
  "issue_date": "string",
  "acknowledgment_date": "string"
}
```

#### Logic Explanation

[Line53](../../po_tracking/views.py): Status being updated to `complete` triggers recalculation of performance metrics, and update of Vendor Table. For more
details regarding metrics calculation see [performance_metrics.md](performance_metrics.md).

### Delete Purchase Order

```http
DELETE /api/purchase_order/{po_number}/
```

#### Response 

```json
{
  "message": "Purchase Order deleted successfully"
}
```

### Acknowledge Purchase Order

```http
POST /api/purchase_order/{po_number}/acknowledge
```

#### Response Body

```json
{
  "message": "Purchase order acknowledged successfully"
}
```

#### Logic Explanation

[Line94](../../po_tracking/views.py) This endpoint triggers recalculation of performance metric: `average_response_time`,
and updates vendor and its performance history. 


Note: Line Nos. are mentioned as per current commits, they are subject to change and may be inconsistent.
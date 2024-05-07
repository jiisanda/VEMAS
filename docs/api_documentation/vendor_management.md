# Vendor Management API

## Contents

- [Model Definitions](#model-definitions)
- [API Endpoints](#api-endpoints)
  - [Create Vendor](#create-vendor)
  - [Get Vendors](#get-vendors)
  - [Get Vendor](#get-vendor)
  - [Update Vendor](#update-vendor)
  - [Delete Vendor](#delete-vendor)
  - [Get Vendor Performance](#get-vendor-performance)

## Model Definitions

```text
Vendor {
  uvc: string [random alphanumeric string of length 6] [unique] [required] [unique vendor code]
  name: string [required] [unique] [vendor name]
  contact_details: TextField [contact details of the vendor]
  address: string [address of the vendor]
  on_time_delivery_rate: float [on time delivery rate of the vendor] [not editable]
  quality_rating: float [quality rating of the vendor] [not editable]
  average_response_time: string [average response time of the vendor] [not editable]
  fulfillment_rate: float [fulfillment rate of the vendor] [not editable]
}

PerformanceHistory {
  date: string [date of the performance history]
  on_time_delivery_rate: float [on time delivery rate of the vendor]
  quality_rating_avg: float [avg quality rating of the vendor]
  average_response_time: string [average response time of the vendor]
  fulfillment_rate: float [fulfillment rate of the vendor]
  vendor: ForeignKey [Vendor.uvc]
}
```

## API Endpoints

### Create Vendor

```http
POST /api/vendors/
```

#### Request Body

```json
{
  "uvc": "string",
  "name": "string",
  "contact_details": "string",
  "address": "string"
}
```

`uvc` gets generated automatically and is a random alphanumeric string of length 6.

#### Response

```json
{
  "uvc": "string",
  "name": "string",
  "contact_details": "string",
  "address": "string",
  "on_time_delivery_rate": 0.0,
  "quality_rating": 0.0,
  "average_response_time": "string",
  "fulfillment_rate": 0.0
}
```

#### Code Explanation

[Line21](../../vendor/views.py) defines the post method for the vendor creation. Have used `APIView` class from `rest_framework.views` to create the API view. The `post` method is used to create a new vendor. The `serializer` class is used to serialize the data and save it to the database.
Could have used `views.generic.CreateAPIView` class to create the API view, but used `APIView` class to have more control over the API view.

### Get Vendors

```http
GET /api/vendors/
```

#### Response

```json
[
  {
    "uvc": "string",
    "name": "string",
    "contact_details": "string",
    "address": "string",
    "on_time_delivery_rate": 0.0,
    "quality_rating": 0.0,
    "average_response_time": "string",
    "fulfillment_rate": 0.0
  }
]
```

#### Code Explanation

[Line 16](../../vendor/views.py) defines the get method for the vendor list. Have used `APIView` class from `rest_framework.views` to create the API view. The `get` method is used to get the list of vendors. The `serializer` class is used to serialize the data and return it as a response.

### Get Vendor

```http
GET /api/vendors/{uvc}/
```

#### Response

```json
{
  "uvc": "string",
  "name": "string",
  "contact_details": "string",
  "address": "string",
  "on_time_delivery_rate": 0.0,
  "quality_rating": 0.0,
  "average_response_time": "string",
  "fulfillment_rate": 0.0
}
```

### Update Vendor

```http
PUT /api/vendors/{uvc}/
```

#### Request Body

```json
{
  "name": "string",
  "contact_details": "string",
  "address": "string"
}
```

#### Response

```json
{
  "uvc": "string",
  "name": "string",
  "contact_details": "string",
  "address": "string",
  "on_time_delivery_rate": 0.0,
  "quality_rating": 0.0,
  "average_response_time": "string",
  "fulfillment_rate": 0.0
}
```

### Delete Vendor

```http
DELETE /api/vendors/{uvc}/
```

#### Response

```json
{
  "message": "Vendor deleted successfully"
}
```

### Get Vendor Performance

```http
GET /api/vendors/{uvc}/performance/
```

#### Response

```json
{
  "history" : [
    {
      "date": "string",
      "on_time_delivery_rate": 0.0,
      "quality_rating_avg": 0.0,
      "average_response_time": "string",
      "fulfillment_rate": 0.0,
      "vendor": "string"
    }
  ]
}
```
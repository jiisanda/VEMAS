from django.urls import path
from .views import VendorsList, VendorsDetail

urlpatterns = [
    path('api/vendors/', VendorsList.as_view(), name='vendor-list'),
    path('api/vendors/<str:pk>/', VendorsDetail.as_view(), name='vendor-detail')
]

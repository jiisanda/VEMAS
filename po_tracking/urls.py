from django.urls import path
from po_tracking.views import POList, PODetail

urlpatterns = [
    path('api/purchase_order/', POList.as_view(), name='po-list'),
    path('api/purchase_order/<str:pk>/', PODetail.as_view(), name='po-detail'),
]
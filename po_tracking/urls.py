from django.urls import path
from po_tracking.views import POList, PODetail, AcknowledgePO

urlpatterns = [
    path('api/purchase_orders/', POList.as_view(), name='po-list'),
    path('api/purchase_orders/<str:pk>/', PODetail.as_view(), name='po-detail'),

    path('api/purchase_orders/<str:pk>/acknowledge', AcknowledgePO.as_view(), name='po-acknowledge'),
]
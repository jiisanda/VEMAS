from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from po_tracking.models import PurchaseOrder
from po_tracking.serializers import POSerializer
from vendor.models import Vendor


# Purchase Order Tracking views here.
class POList(APIView):
    """
    List all po_orders, or create new po_orders
    """
    def get(self, request):
        po_list = PurchaseOrder.objects.all()
        serializer = POSerializer(po_list, many=True)
        return Response(serializer.data)

    def post(self, request):
        uvc = request.data.get('vendor')
        try:
            Vendor.objects.get(uvc=uvc)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = POSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PODetail(APIView):
    """
    Retrieve, update, or delete a po_order
    """
    def get_object(self, pk):
        ...

    def get(self, request, pk):
        ...

    def put(self, request, pk):
        ...

    def delete(self, request, pk):
        ...

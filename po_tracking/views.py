from django.http import Http404
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
        try:
            return PurchaseOrder.objects.get(po_number=pk)
        except PurchaseOrder.DoesNotExist:
            return Http404

    def get(self, request, pk):
        po = self.get_object(pk)
        serializer = POSerializer(po)
        return Response(serializer.data)

    def put(self, request, pk):
        po = self.get_object(pk)
        serializer = POSerializer(po, data=request.data, partial=True)
        if serializer.is_valid():
            # todo: @jiisanda: check weather status got changed
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        po = self.get_object(pk)
        try:
            po.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AttributeError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': f"{pk} does not exist."})

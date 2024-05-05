from django.http import Http404
from django.db.models import Avg, ExpressionWrapper, F, DurationField
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from po_tracking.helper import update_metrics, update_vendor_and_history
from po_tracking.models import PurchaseOrder
from po_tracking.serializers import POSerializer, POSerializerCreate
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

        serializer = POSerializerCreate(data=request.data)
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
        # todo: @jiisanda: proper error handling here
        po = self.get_object(pk)
        serializer = POSerializer(po, data=request.data, partial=True)

        if serializer.is_valid():
            current_status = po.status
            new_status = serializer.validated_data.get('status')

            if current_status != new_status and new_status == 'completed':
                if serializer.validated_data.get('quality_rating') is None:
                    return Response({'error': 'Quality rating are required to complete the PO'},
                                    status=status.HTTP_400_BAD_REQUEST)

                po.actual_delivery_date = timezone.now()
                po.save()

            if serializer.validated_data.get('expected_delivery_date'):
                po.expected_delivery_date = serializer.validated_data.get('expected_delivery_date')
                po.save()

            serializer.save()

            metrics = update_metrics(po.vendor)
            update_vendor_and_history(vendor=po.vendor.uvc, metrics=metrics)

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


class AcknowledgePO(APIView):
    """
    Acknowledge Purchase order
    """
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.get(po_number=pk)
        except PurchaseOrder.DoesNotExist:
            return Http404

    def post(self, request, pk):
        po = self.get_object(pk)
        vendor = po.vendor

        # update acknowledgment_date in Purchase order
        po.acknowledgment_date = timezone.now()
        po.save()

        # update the average_response_time for vendor
        average_response_time = PurchaseOrder.objects.filter(vendor=vendor, acknowledgment_date__isnull=False).aggregate(
            avg_response_time=Avg(
                ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())
            )
        )['avg_response_time']

        new_metrics = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate
        }

        update_vendor_and_history(vendor=vendor.uvc, metrics=new_metrics)

        return Response({'message': 'Purchase order acknowledged successfully'}, status=status.HTTP_200_OK)

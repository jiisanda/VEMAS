from django.shortcuts import render
from rest_framework.views import APIView


# Purchase Order Tracking views here.
class POList(APIView):
    """
    List all po_orders, or create new po_orders
    """
    def get(self, request):
        ...

    def post(self, request):
        ...


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

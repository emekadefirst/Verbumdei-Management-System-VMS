from django.http import Http404
from .models import Voucher
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import VourcherSerializers


class VoucherView(APIView):
    def get(self, request):
        obj = Voucher.objects.all()
        serializer = VourcherSerializers(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = VourcherSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VoucherDetailView(APIView):
    def get_object(self, pk):
        try:
            return Voucher.objects.get(pk=pk)
        except Voucher.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        voucher = self.get_object(pk)
        serializer = VourcherSerializers(voucher)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        voucher = self.get_object(pk)
        serializer = VourcherSerializers(voucher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

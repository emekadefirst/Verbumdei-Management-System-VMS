import os
from django.core.exceptions import ValidationError
from django.http import Http404
from .models import Payment, PaymentType
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PaymentSerializers, PaymentTypeSerializer
from parent.models import Parent
from parent.serializers import ParentSerializer
from pypstk.payment import Payment as PaystackPayment
from dotenv import load_dotenv

load_dotenv()

secret_key = os.environ.get("SECRET_KEY")


class PaymentTypeView(APIView):
    def get(self, request, format=None):
        type = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(type, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PaymentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllPaymentView(APIView):
    def get(self, request, format=None):
        payment = Payment.objects.all()
        serializer = PaymentSerializers(payment, many=True)
        return Response(serializer.data)



class PaymentDetailView(APIView):
    def get_object(self, pk):
        try:
            return Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        payment = self.get_object(pk)
        serializer = PaymentSerializers(payment)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        payment = self.get_object(pk)
        serializer = PaymentSerializers(payment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

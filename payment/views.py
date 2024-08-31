import os
from django.core.exceptions import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
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


# class MakePaymentView(APIView):
#     def post(self, request, parent_id):
#         parent = get_object_or_404(Parent, code=parent_id)
#         email = parent.email

#         serializer = PaymentSerializers(data=request.data)
#         if serializer.is_valid():
#             payment_type_name = serializer.validated_data["payment_type"]

#             # Fetch the payment type object using the name
#             payment_type = PaymentType.objects.filter(name=payment_type_name).first()
#             if not payment_type:
#                 return Response(
#                     {"error": "Payment type not found"},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )

#             # Retrieve the amount associated with the payment type
#             amount = payment_type.cost  # Use 'amount' if that is the field name

#             # Initialize the transaction with Paystack
#             secret_key = os.getenv("SECRET_KEY")
#             if not secret_key:
#                 return Response(
#                     {"error": "Paystack secret key is not set"},
#                     status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                 )

#             try:
#                 paystack_payment = Payment(
#                     email, amount, secret_key
#                 )
#                 payment_response = paystack_payment.initialize_transaction()

#                 if isinstance(payment_response, dict):
#                     reference_id = payment_response.get("references")
#                     payment_url = payment_response.get("url")

#                     if not reference_id or not payment_url:
#                         return Response(
#                             {
#                                 "error": "Payment initialization failed or invalid response"
#                             },
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                         )

#                     serializer.save(parent=parent, reference_id=reference_id)

#                     return Response(
#                         {"payment_url": payment_url}, status=status.HTTP_201_CREATED
#                     )
#                 else:
#                     return Response(
#                         {"error": "Unexpected response format from Paystack"},
#                         status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                     )
#             except Exception as e:
#                 return Response(
#                     {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#                 )
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

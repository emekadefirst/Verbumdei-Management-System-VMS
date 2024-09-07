import os
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from .serializers import PaymentSerializers
from pypstk.payment import Payment
from dotenv import load_dotenv

load_dotenv()

secret_key = os.environ.get("PAYSTACK_KEY")


class MakePaymentView(APIView):
    def post(self, request):
        serializer = PaymentSerializers(data=request.data)
        if serializer.is_valid():
            payment_type = serializer.validated_data.get("payment_type")
            parent = serializer.validated_data.get("parent")

            if not payment_type or not parent:
                return JsonResponse(
                    {"error": "Invalid payment or parent data"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            amount = payment_type.amount * 100
            email = parent.email

            if not secret_key:
                return JsonResponse(
                    {"error": "Secret key not found"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            try:
                pay = Payment(
                    email, amount, secret_key
                )
                response = pay.initialize_transaction()
                reference = response["references"]
                payment = serializer.save(reference=reference)
                url  = response["url"]
                return JsonResponse(url, safe=False, status=status.HTTP_200_OK)
            except Exception as e:
                print(f"Error initializing transaction: {e}")
                return JsonResponse(
                    {"error": "Payment initialization failed"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return JsonResponse(
            {"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST
        )

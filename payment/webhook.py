import os
from dotenv import load_dotenv
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from .models import Payment, PaymentType  # Assuming these models are defined
from django.conf import settings
import hashlib
import hmac
import json

load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_KEY")


class Verify(APIView):
    def post(self, request):
        paystack_signature = request.headers.get("X-Paystack-Signature")
        if not paystack_signature:
            return JsonResponse(
                {"error": "Signature missing"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Verifying Paystack signature
        if not self.verify_paystack_signature(request.body, paystack_signature):
            return JsonResponse(
                {"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST
            )

        data = json.loads(request.body)
        event = data.get("event")

        if event == "paymentrequest.success":
            # Assuming 'reference' is a field in your Payment model
            reference = data["data"].get("offline_reference")

            # Fetch the payment record using the reference
            try:
                payment = Payment.objects.get(reference=reference)
                payment.status = "successful"
                payment.save()
                # Additional processing if needed
            except Payment.DoesNotExist:
                return JsonResponse(
                    {"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND
                )

        return JsonResponse({"status": "received"}, status=status.HTTP_200_OK)

    def verify_paystack_signature(self, payload, signature):
        secret = PAYSTACK_SECRET_KEY
        computed_signature = hmac.new(
            secret.encode("utf-8"), msg=payload, digestmod=hashlib.sha512
        ).hexdigest()
        return hmac.compare_digest(computed_signature, signature)

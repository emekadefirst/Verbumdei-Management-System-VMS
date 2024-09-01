import hmac
import hashlib
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings


# Function to verify the signature of the incoming request
def verify_signature(request):
    secret_key = settings.PAYSTACK_SECRET_KEY
    signature = request.headers.get("x-paystack-signature")
    if not signature:
        return False

    payload = request.body
    hash = hmac.new(secret_key.encode("utf-8"), payload, hashlib.sha512).hexdigest()
    return hmac.compare_digest(signature, hash)


class PaystackWebhookView(APIView):
    def post(self, request):
        if not verify_signature(request):
            return JsonResponse(
                {"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST
            )
        try:
            event = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse(
                {"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST
            )
        event_type = event.get("event")
        if event_type == "charge.success":
            self.handle_charge_success(event)
        elif event_type == "refund.processed":
            self.handle_refund_processed(event)
        elif event_type == "subscription.create":
            self.handle_subscription_create(event)
        else:
            return JsonResponse(
                {"error": "Unhandled event type"}, status=status.HTTP_400_BAD_REQUEST
            )

        return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)

    # def handle_charge_success(self, event):
    #     # Implement your logic for a successful charge
    #     pass

    # def handle_refund_processed(self, event):
    #     # Implement your logic for a processed refund
    #     pass

    # def handle_subscription_create(self, event):
    #     # Implement your logic for a new subscription
    #     pass

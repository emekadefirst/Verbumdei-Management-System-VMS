#Generate secret keys

#Run
"./manage.py shell" or "python manage.py shell"
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

{
  "username": "test_user",
  "password": "test_password",
  "email": "test@example.com"
}

./manage.py makemigrations api --empty
Migrations for 'api':
  api\migrations\0001_initial.py


gunicorn --workers 3 --bind 0.0.0.0:8000 server.wsgi:application --env DJANGO_SETTINGS_MODULE=server.settings.production
gunicorn server.wsgi:application
gunicorn server.wsgi:application --workers 3 --bind 0.0.0.0:8000


{
    "parent": "vb20827pa15",
    "payment_type": "First Term School Fee",
    "student": "VD20240827155323",
    "method": "CASH"
}
https://verbumdei-management-system-vms.onrender.com/payment/make-payment/



{
  "event": "paymentrequest.success",
  "data": {
    "id": 1089700,
    "domain": "test",
    "amount": 10000000,
    "currency": "NGN",
    "due_date": null,
    "has_invoice": false,
    "invoice_number": null,
    "description": "Pay up now",
    "pdf_url": null,
    "line_items": [],
    "tax": [],
    "request_code": "PRQ_y0paeo93jh99mho",
    "status": "success",
    "paid": true,
    "paid_at": "2019-06-21T15:26:10.000Z",
    "metadata": null,
    "notifications": [
      {
        "sent_at": "2019-06-21T15:25:42.452Z",
        "channel": "email"
      }
    ],
    "offline_reference": "3365451089700",
    "customer": 7454223,
    "created_at": "2019-06-21T15:25:42.000Z"
  }
}

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

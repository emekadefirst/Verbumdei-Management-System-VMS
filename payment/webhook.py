import hmac
import hashlib
import json
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Payment


# @csrf_exempt
@require_POST
def paystack_webhook(request):
    paystack_secret = settings.PAYSTACK_SECRET_KEY

    # Validate event
    payload = request.body
    signature = request.headers.get("X-Paystack-Signature")

    if not signature:
        return HttpResponse("No signature provided", status=400)

    # Verify signature
    computed_hmac = hmac.new(
        paystack_secret.encode("utf-8"), payload, hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(computed_hmac, signature):
        return HttpResponse("Invalid signature", status=400)

    # Parse the event data
    event = json.loads(payload)

    # Check if it's a charge.success event
    if event["event"] == "charge.success":
        try:
            # Extract relevant information
            reference = event["data"]["reference"]
            status = event["data"]["status"]

            # Update the payment status in your database
            payment = Payment.objects.get(reference=reference)
            payment.status = status
            payment.save()

            print(f"Payment {reference} updated to {status}")
            return HttpResponse(status=200)
        except Payment.DoesNotExist:
            print(f"Payment with reference {reference} not found")
            return HttpResponse("Payment not found", status=404)
        except Exception as e:
            print(f"Error processing webhook: {str(e)}")
            return HttpResponse("Error processing webhook", status=500)

    # For other event types, just acknowledge receipt
    return HttpResponse(status=200)

import hmac
import hashlib
import json
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Payment


@require_POST
def paystack_webhook(request):
    paystack_secret = settings.PAYSTACK_SECRET_KEY
    payload = request.body
    signature = request.headers.get("X-Paystack-Signature")
    if not signature:
        return HttpResponse("No signature provided", status=400)
    computed_hmac = hmac.new(
        paystack_secret.encode("utf-8"), payload, hashlib.sha512
    ).hexdigest()

    if not hmac.compare_digest(computed_hmac, signature):
        return HttpResponse("Invalid signature", status=400)
    event = json.loads(payload)
    if event["event"] == "charge.success":
        try:
            reference = event["data"]["reference"]
            status = event["data"]["status"]
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
    return HttpResponse(status=200)

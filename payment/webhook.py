import os
from dotenv import load_dotenv
import hashlib
import hmac
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Payment
load_dotenv()

@csrf_exempt
@require_http_methods(["POST"])
def verify_payment(request):
    paystack_signature = request.headers.get("x-paystack-signature", "")
    if not paystack_signature:
        return JsonResponse({"error": "Signature not provided"}, status=400)
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)
    secret_key = os.getenv("PAYSTACK_KEY")
    computed_signature = hmac.new(
        secret_key.encode("utf-8"), request.body, hashlib.sha512
    ).hexdigest()
    if computed_signature != paystack_signature:
        return JsonResponse({"error": "Signature mismatch"}, status=400)
    event = payload.get("event")
    data = payload.get("data", {})

    if event == "charge.success" and data.get("status") == "success":
        reference = data.get("reference")
        try:
            payment = Payment.objects.get(reference=reference)
            payment.status = "success"
            payment.save()

            return JsonResponse(
                {"message": "Payment verification successful"}, status=200
            )
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)

    return JsonResponse({"error": "Payment verification failed"}, status=400)

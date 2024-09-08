from .paystack import secret_key
import hashlib
import hmac
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Payment
import requests
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .models import Payment

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


def paystack_callback(request):
    reference = request.GET.get("reference")
    if not reference:
        return JsonResponse({"error": "No reference provided"}, status=400)

    # Verify payment with Paystack API
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}
    url = f"https://api.paystack.co/transaction/verify/{reference}"

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return JsonResponse({"error": "Failed to verify payment"}, status=500)

    result = response.json()

    if result["data"]["status"] == "success":
        # Payment is successful, update your database accordingly
        try:
            payment = Payment.objects.get(reference=reference)
            payment.status = "success"
            payment.save()
            # You can render a success page or redirect
            return HttpResponse("Payment successful")
        except Payment.DoesNotExist:
            return JsonResponse({"error": "Payment not found"}, status=404)

    return JsonResponse({"error": "Payment verification failed"}, status=400)

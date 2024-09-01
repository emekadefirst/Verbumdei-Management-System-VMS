from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from .models import Payment, PaymentType

def hook(request):
    pass

# class Verify(APIView):
#     def post(self, request):
#         data = request.data
#         status_response = data.get("event")

#         if status_response == "paymentrequest.success":
#             try:
#                 # Check if a payment with this transaction_id or reference already exists
#                 if Payment.objects.filter(reference=data.get("reference")).exists():
#                     return JsonResponse(
#                         {"status": "duplicate"}, status=status.HTTP_200_OK
#                     )

#                 payment_type = PaymentType.objects.get(name=data.get("payment_type"))

#                 payment = Payment(
#                     transaction_id=data.get("transaction_id"),
#                     status=data.get("status", "processing"),
#                     payment_type=payment_type,
#                     parent_id=data.get("parent_id"),
#                     student_id=data.get("student_id"),
#                     method=data.get("method"),
#                     reference=data.get("reference"),
#                 )
#                 payment.save()
#             except PaymentType.DoesNotExist:
#                 return JsonResponse(
#                     {"error": "Invalid payment type"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             except Exception as e:
#                 return JsonResponse(
#                     {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#                 )

#         print("Received webhook data:", data)
#         return JsonResponse({"status": "success"}, status=status.HTTP_200_OK)

{
    "email": "test@mail.com",
    "phone_number_1": "3254678980",
    "phone_number_2": "43278964835",
    "parent_name": "Ogunmekpon",
    "home_address": "This field is required."
}

from django.urls import path
from .paystack import  MakePaymentView
from .views import PaymentTypeView, AllPaymentView, PaymentDetailView
from .webhook import Verify

urlpatterns = [
    path("payment-types/", PaymentTypeView.as_view(), name="payment-types"),
    path("payments/", AllPaymentView.as_view(), name="all-payments"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("make-payment/", MakePaymentView.as_view(), name="make-payment"),
    path("webhook/", Verify.as_view(), name="paystack_webhook"),
]

# {
#     "parent": "vb20240901pa053607",
#     "payment_type": "Excursion",
#     "student": "VD20240827155323",
#     "method": "ONLINE"
# }

from django.urls import path
from .paystack import  MakePaymentView
from .views import PaymentTypeView, AllPaymentView, PaymentDetailView
from .webhook import paystack_webhook

urlpatterns = [
    path("payment-types/", PaymentTypeView.as_view(), name="payment-types"),
    path("payments/", AllPaymentView.as_view(), name="all-payments"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("make-payment/", MakePaymentView.as_view(), name="make-payment"),
    path("webhook/", paystack_webhook, name="paystack_webhook"),
]

# {
#     "parent": "vb20827pa15",
#     "payment_type": "First Term School Fee",
#     "student": "VD20240827155323",
#     "method": "CASH"
# }

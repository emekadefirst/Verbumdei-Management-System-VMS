from django.urls import path
from .views import PaymentTypeView, AllPaymentView, MakePaymentView, PaymentDetailView

urlpatterns = [
    path("payment-types/", PaymentTypeView.as_view(), name="payment-types"),
    path("payments/", AllPaymentView.as_view(), name="all-payments"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("make-payment/<int:pk>/", MakePaymentView.as_view(), name="make-payment"),
]

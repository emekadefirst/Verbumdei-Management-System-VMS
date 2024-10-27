from django.urls import path
from .paystack import  MakePaymentView
from .views import PaymentTypeView, AllPaymentView, PaymentDetailView, PhysicalView, PhysicalPaymentView, TotalPayment, TotalTuitionForMonth, StudentPaymentHistory, TotalDeptTheMonthView
# from .webhook import verify_payment, paystack_callback

urlpatterns = [
    path("payment-types/", PaymentTypeView.as_view(), name="payment-types"),
    path("payments/", AllPaymentView.as_view(), name="all-payments"),
    path("payments/<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    path("make-payment/", MakePaymentView.as_view(), name="make-payment"),
    # path("webhook/", verify_payment, name="paystack_webhook"),
    # path("callback/", paystack_callback, name="paystack_callback"),
    # physical
    path('physical-payments/', PhysicalView.as_view(), name='physical-payments-list-create'),
    path('physical-payments/<int:pk>/', PhysicalPaymentView.as_view(), name='physical-payment-detail'),
    path('total-payment/', TotalPayment.as_view(), name='total-payment'),
    path('total-tuition/', TotalTuitionForMonth.as_view(), name='total-tuition'),
    path('total-dept/', TotalDeptTheMonthView.as_view(), name='total-tuition'),
    path('student-payment/<str:registration_id>/', StudentPaymentHistory.as_view(), name='student')  
]



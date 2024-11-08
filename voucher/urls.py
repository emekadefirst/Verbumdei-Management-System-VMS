from django.urls import path
from . import views

urlpatterns = [
    path("", views.VoucherView.as_view(), name="create-voucher"),
    path("<int:pk>/", views.VoucherDetailView.as_view(), name="voucher-detail"),
]
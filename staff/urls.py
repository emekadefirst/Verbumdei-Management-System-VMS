from django.urls import path
from .views import (
    StaffListCreateAPIView, StaffDetailAPIView,
    AccountInfoListCreateAPIView, AccountInfoDetailAPIView,
    PayrollListCreateAPIView, PayrollDetailAPIView, PayrollExportAPIView, AccountCountView,
    StaffCountView,
)

urlpatterns = [
    path('staff/', StaffListCreateAPIView.as_view(), name='staff-list-create'),
    path('staff/<int:pk>/', StaffDetailAPIView.as_view(), name='staff-detail'),
    path('staff-count/', StaffCountView.as_view(), name='staff-count'),
    path('account-count/', AccountCountView.as_view(), name='account-count'),
    path('account-info/', AccountInfoListCreateAPIView.as_view(), name='account-info-list-create'),
    path('account-info/<int:pk>/', AccountInfoDetailAPIView.as_view(), name='account-info-detail'),
    path('payroll/', PayrollListCreateAPIView.as_view(), name='payroll-list-create'),
    path('payroll/<int:pk>/', PayrollDetailAPIView.as_view(), name='payroll-detail'),
    path('payroll/export/<str:pay_period>/', PayrollExportAPIView.as_view(), name='payroll-export'),
]

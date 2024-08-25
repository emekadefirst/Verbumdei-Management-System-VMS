from django.urls import path
from .views import *

urlpatterns = [
    path('all-type/', InventoryTypeView.as_view(), name='inventory-type-list-create'),
    path('type/<int:pk>/', InventoryTypeDetailView.as_view(), name='inventory-detail'),
    path('all-inventory/', InventoryView.as_view(), name='inventory-list-create'),
    path('count/', InventoryCountView.as_view(), name='inventory-count'),
    path('inventory/<int:pk>/', InventoryDetailAPIView.as_view(), name='inventory'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.SubAdminView.as_view(), name="create"),
    path('login/', views.StaffLoginView.as_view(), name='login'),
]

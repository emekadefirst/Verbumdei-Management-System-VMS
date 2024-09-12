from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SubAdminView.as_view(), name="create"),
    path("login/", views.SubAdminLoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]

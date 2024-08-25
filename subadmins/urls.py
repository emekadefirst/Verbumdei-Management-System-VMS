from django.urls import path
from .views import SignupView, LoginView, LogoutView, PasswordResetView

urlpatterns = [
    path('api/auth/signup/', SignupView.as_view(), name='signup'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/password-reset/', PasswordResetView.as_view(), name='password_reset'),
]

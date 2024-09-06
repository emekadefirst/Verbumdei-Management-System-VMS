from django.urls import path
from .views import RegisterUser, LoginUser, LogoutUser

urlpatterns = [
    path("signup/", RegisterUser.as_view(), name="signup"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout/", LogoutUser.as_view(), name="logout"),
    # path('api/auth/password-reset/', PasswordResetView.as_view(), name='password_reset'),
]

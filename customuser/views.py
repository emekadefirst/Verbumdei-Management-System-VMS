from rest_framework.views import APIView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication

class SignupView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)  
            return Response(
                {"token": token.key, "user": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                "token": token.key,
                "user_id": user.id,
                "role": user.role,
                "username": user.username,
                "person_id": user.person_id,
                "email": user.email,
            }

            if user.first_name:
                response_data["first_name"] = user.first_name
            if user.last_name:
                response_data["last_name"] = user.last_name

            # login_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            # email_subject = "Login Alert"
            # email_html_message = render_to_string(
            #     "login.html",
            #     {
            #         "user_name": (
            #             f"{user.first_name} {user.last_name}"
            #             if user.first_name
            #             else user.username
            #         ),
            #         "role": user.role,
            #         "time": login_time,
            #         "ip_address": request.META.get("REMOTE_ADDR", "Unknown IP Address"),
            #     },
            # )
            # send_mail(
            #     subject=email_subject,
            #     message="Login Notification",
            #     from_email="verbumdei85@gmail.com",  
            #     recipient_list=[user.email],
            #     fail_silently=False,
            #     html_message=email_html_message,
            # )
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            return Response({"error": "Invalid token or already logged out."}, status=status.HTTP_400_BAD_REQUEST,)
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

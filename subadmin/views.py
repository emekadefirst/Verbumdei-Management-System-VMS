from .models import SubAdmin
from django.contrib.auth import authenticate, login
from .serializers import SubAdminSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout


class SubAdminView(APIView):
    def post(self, request, format=None):
        serializer = SubAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.exceptions import ValidationError


class SubAdminLoginView(APIView):
    def post(self, request, format=None):
        admin_id = request.data.get("admin_id")
        password = request.data.get("password")
        if not admin_id:
            return Response(
                {"error": "Admin ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = SubAdmin.objects.get(admin_id=admin_id)
        except SubAdmin.DoesNotExist:
            return Response(
                {"error": "Invalid credentials, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(password):

            return Response(
                {"error": "Invalid credentials, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        login(request, user)
        serializer = SubAdminSerializer(user)

        return Response(
            {"user": serializer.data, "message": "Login successful"},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    def post(self, request, format=None):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

from .models import SubAdmin
from django.contrib.auth import authenticate, login
from .serializers import SubAdminSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SubAdminView(APIView):
    def post(self, request, format=None):
        serializer = SubAdminSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffLoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )

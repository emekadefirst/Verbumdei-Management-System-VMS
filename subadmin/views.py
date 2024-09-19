from .models import SubAdmin
from django.contrib.auth import authenticate, login, logout
from .serializers import SubAdminSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from staff.models import Staff
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication


class SubAdminView(APIView):
    def post(self, request, format=None):
        serializer = SubAdminSerializer(data=request.data)
        if serializer.is_valid():
            subadmin = serializer.save()
            token = Token.objects.create(user=subadmin)  
            return Response(
                {"token": token.key, "subadmin": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubAdminLoginView(APIView):
    permission_classes = [AllowAny]
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
            staff_profile = Staff.objects.get(staff_id=admin_id)
            profile_image = staff_profile.img_url
        except SubAdmin.DoesNotExist:
            return Response(
                {"error": "Invalid credentials, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Staff.DoesNotExist:
            return Response(
                {"error": "Staff profile not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request, user)
        serializer = SubAdminSerializer(user)
        user_data = serializer.data
        user_data["profile_image"] = profile_image

        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {"token": token.key, "user": user_data, "message": "Login successful"},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]  
    permission_classes = [IsAuthenticated]  

    def post(self, request, format=None):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  
        except Token.DoesNotExist:
            return Response({"error": "Invalid token or already logged out."}, status=status.HTTP_400_BAD_REQUEST)
        logout(request)

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

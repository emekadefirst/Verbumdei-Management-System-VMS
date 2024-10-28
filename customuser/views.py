from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsAccountant, IsHeadTeacher, IsParent, IsTeacher
from .models import CustomUser
from staff.models import Staff
from parent.models import Parent
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
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
    def post(self, request, format=None):
        person_id = request.data.get("person_id")
        password = request.data.get("password")

        if not person_id:
            return Response(
                {"error": "ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                {"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = CustomUser.objects.get(person_id=person_id)
            profile_image = None

            try:
                staff_profile = Staff.objects.get(staff_id=person_id)
                profile_image = staff_profile.img_url
            except Staff.DoesNotExist:
                try:
                    parent_profile = Parent.objects.get(code=person_id)
                    profile_image = parent_profile.img_url
                except Parent.DoesNotExist:
                    return Response(
                        {"error": "Invalid credentials, please try again."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # Authenticate user with person_id and password
            user = authenticate(username=user.username, password=password)
            if not user:
                return Response(
                    {"error": "Invalid credentials, please try again."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            login(request, user)

            serializer = UserSerializer(user)
            user_data = serializer.data
            user_data["profile_image"] = profile_image or None
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user": user_data, "message": "Login successful"},
                status=status.HTTP_200_OK,
            )

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid credentials, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )


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

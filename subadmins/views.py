from .serializers import SubAdminSerializer, SubAdminLoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny



class RegisterUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SubAdminSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            login(request, user)  
            user_data = {
                "username": user.username,
                "email": user.email,
                "id": user.id,
            }
            return Response(
                {
                    "message": "Registration successful",
                    "token": token.key,
                    "user": user_data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SubAdminLoginSerializer(
            data=request.data
        )  # Changed to login serializer
        if serializer.is_valid():
            username = serializer.data.get("username")
            password = serializer.data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)

                return Response(
                    {
                        "token": token.key,
                        "user_id": user.id,
                        "username": user.username,
                        "email": user.email,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the user's token
        try:
            token = Token.objects.get(user=request.user)
            # Delete the token to log the user out
            token.delete()
            return Response(
                {"message": "Logout successful."}, status=status.HTTP_200_OK
            )
        except Token.DoesNotExist:
            return Response(
                {"error": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST
            )

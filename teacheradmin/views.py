from .models import TeacherAdmin
from .serializers import TeacherSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout, login
from staff.models import Staff
from grade.models import Subject, Class
from student.models import Student
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class TeacherView(APIView):
    def post(self, request, format=None):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save() 
            return Response(
                {"teacher": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherLoginView(APIView):
    def post(self, request, format=None):
        teacher_id = request.data.get("teacher_id")
        password = request.data.get("password")

        if not teacher_id:
            return Response({"error": "Teacher ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = TeacherAdmin.objects.get(teacher_id=teacher_id)
            staff_profile = Staff.objects.get(staff_id=teacher_id)
            profile_image = staff_profile.img_url

            class_profile = Class.objects.filter(teacher=staff_profile).first()
            class_name = class_profile.name if class_profile else None
            students = Subject.objects.filter(teacher=staff_profile.id) if class_profile else []
            student_count = students.count()

            subjects_assigned = Subject.objects.filter(teacher=staff_profile)
            subject_names = [subject.name for subject in subjects_assigned]
        except TeacherAdmin.DoesNotExist:
            return Response({"error": "Invalid credentials, please try again."}, status=status.HTTP_400_BAD_REQUEST)
        except Staff.DoesNotExist:
            return Response({"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials, please try again."}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        serializer = TeacherSerializer(user)
        user_data = serializer.data
        user_data.update({
            "profile_image": profile_image,
            "class_assigned": class_name,
            "subjects_assigned": subject_names,
            "student_count": student_count,
        })

        return Response({
            "user": user_data,
            "message": "Login successful"
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

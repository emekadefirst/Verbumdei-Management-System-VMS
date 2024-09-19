from .models import TeacherAdmin
from .serializers import TeacherSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout, login
from staff.models import Staff
from grade.models import Subject, Class, SubjectMaterial
from student.models import Student
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication


class TeacherView(APIView):
    def post(self, request, format=None):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        teacher_id = request.data.get("teacher_id")
        password = request.data.get("password")

        if not teacher_id:
            return Response(
                {"error": "Teacher ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = TeacherAdmin.objects.get(teacher_id=teacher_id)
            staff_profile = Staff.objects.get(staff_id=teacher_id)
            profile_image = staff_profile.img_url
            try:
                class_profile = Class.objects.get(teacher=staff_profile)
                class_name = class_profile.name
                class_instance = class_profile
            except Class.DoesNotExist:
                class_name = None
                class_instance = None
            if class_instance:
                students = Student.objects.filter(class_assigned=class_instance)
                student_count = students.count()
                student_info = [
                    f"{student.first_name} {student.last_name} - {student.registration_id}"
                    for student in students
                ]
                student_profile_images = [student.img_url for student in students]
            else:
                student_info = []
                student_profile_images = []
                student_count = 0

            subjects_assigned = Subject.objects.filter(teacher=staff_profile)
            subject_names = [subject.name for subject in subjects_assigned]

            materials = []
            for subject in subjects_assigned:
                subject_materials = SubjectMaterial.objects.filter(subject=subject)
                materials.extend(
                    [material.material_url for material in subject_materials]
                )

        except TeacherAdmin.DoesNotExist:
            return Response(
                {"error": "Invalid credentials, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Staff.DoesNotExist:
            return Response(
                {"error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND
            )


        if not user.check_password(password):
            return Response(
                {"error": "Invalid credentials, please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        login(request, user)
        serializer = TeacherSerializer(user)
        user_data = serializer.data
        user_data.update(
            {
                "profile_image": profile_image,
                "class_assigned": class_name,
                "subjects_assigned": subject_names,
                "student_count": student_count,
                "students": student_info,
                "students_image": student_profile_images,
                "subject_material": materials,
            }
        )
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
            return Response(
                {"error": "Invalid token or already logged out."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        logout(request)

        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

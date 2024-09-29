from grade.models import Class
from student.models import Student
from .models import Attendance
from staff.models import Staff
from rest_framework import status
from teacheradmin.models import TeacherAdmin
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import AttendanceSerializer
from datetime import date


class CreateAttendanceView(APIView):
    def post(self, request, staff_id, format=None):
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            teacher = get_object_or_404(TeacherAdmin, teacher_id=staff_id)
            confirm_if_staff = get_object_or_404(Staff, staff_id=staff_id)
            assigned_class = get_object_or_404(Class, teacher=confirm_if_staff)
            if teacher and confirm_if_staff and assigned_class:
                student_id = serializer.validated_data.get("student")
                day_marked = serializer.validated_data.get("date", date.today())  
                attendance_exists = Attendance.objects.filter(
                    student__registration_id=student_id, date=day_marked
                ).exists()

            if attendance_exists:
                return Response(
                    {
                        "error": "Attendance for this student has already been taken. Comeback tomorrow"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllAttendanceView(APIView):
    def get(self, request):
        attendance = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance, many=True)
        return Response(serializer.data)


class AttendanceByClassView(APIView):
    def get(self, request, staff_id):
        teacher = get_object_or_404(Staff, staff_id=staff_id, staff_type="TEACHING")
        assigned_class = Class.objects.filter(teacher=teacher).first() 
        if assigned_class:
            attendance_records = Attendance.objects.filter(grade=assigned_class)
            serializer = AttendanceSerializer(attendance_records, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "No class found for this teacher."},
                status=status.HTTP_404_NOT_FOUND,
            )


class AttendanceByStudent(APIView):
    def get(self, request, student_id):
        student = get_object_or_404(Student, registration_id=student_id)
        attendance_records = Attendance.objects.filter(student=student)
        total_attendance = sum(record.count for record in attendance_records)
        serializer = AttendanceSerializer(attendance_records, many=True)
        return Response(
            {
                "attendance_records": serializer.data,
                "total_attendance": total_attendance,
            },
            status=status.HTTP_200_OK,
        )


class UpdateAttendanceView(APIView):
    def put(self, request, staff_id, format=None):
        teacher = get_object_or_404(TeacherAdmin, teacher_id=staff_id)
        student_id = request.data.get("registration_id")
        if not student_id:
            return Response(
                {"error": "Student ID is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        student = get_object_or_404(Student, registration_id=student_id)
        assigned_class = Class.objects.filter(teacher=teacher, students=student).first()
        if not assigned_class:
            return Response(
                {"error": "Teacher is not assigned to this student's class."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        attendance_record = get_object_or_404(
            Attendance, student=student, grade=assigned_class
        )
        serializer = AttendanceSerializer(
            attendance_record, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

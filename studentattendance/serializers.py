from .models import Attendance
from .models import Student
from .models import Class
from rest_framework import serializers


class ClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ["name"]

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["registration_id"]


class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.CharField()  # Accepts the student registration ID as a string
    grade = serializers.CharField()  # Accepts the grade name as a string

    class Meta:
        model = Attendance
        fields = ["id", "student", "grade", "date", "present", "created_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }

    
    def create(self, validated_data):
        # Retrieve student and grade using the provided string values
        student = Student.objects.get(registration_id=validated_data.pop("student"))
        grade = Class.objects.get(name=validated_data.pop("grade"))

        # Create the Attendance record
        attendance = Attendance.objects.create(
            student=student, grade=grade, **validated_data
        )
        return attendance

    def update(self, instance, validated_data):
        # Update the student and grade if provided
        student_value = validated_data.pop("student", None)
        grade_value = validated_data.pop("grade", None)

        if student_value:
            instance.student = Student.objects.get(registration_id=student_value)
        if grade_value:
            instance.grade = Class.objects.get(name=grade_value)

        return super().update(instance, validated_data)

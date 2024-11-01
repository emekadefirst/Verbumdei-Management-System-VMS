from .models import Attendance
from .models import Student
from .models import Class
from rest_framework import serializers

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(slug_field="registration_id", queryset=Student.objects.all()) 
    grade = serializers.SlugRelatedField(slug_field="name", queryset=Class.objects.all())  

    class Meta:
        model = Attendance
        fields = ["id", "student", "grade", "date", "present", "created_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }

    
    def create(self, validated_data):
        attendance = Attendance.objects.create(**validated_data)
        return attendance

    def update(self, instance, validated_data):
        student_value = validated_data.pop("student", None)
        grade_value = validated_data.pop("grade", None)

        if student_value:
            instance.student = Student.objects.get(registration_id=student_value)
        if grade_value:
            instance.grade = Class.objects.get(name=grade_value)

        return super().update(instance, validated_data)
    
    
class GetAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

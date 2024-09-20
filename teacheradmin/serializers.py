from rest_framework import serializers
from .models import TeacherAdmin
from staff.models import Staff
from datetime import datetime


def userId(firstname):
    now = datetime.now()
    return f"{firstname}{now.strftime('%M%S')}"


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAdmin
        fields = [
            "staff_id",
            "username",
            "password",
            "teacher_id",
            "created_at",
            "first_name",
            "last_name",
            "email",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "teacher_id": {"read_only": True},
            "created_at": {"read_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "email": {"read_only": True},
            "username": {"read_only": True},
        }

    def create(self, validated_data):
        staff_id = validated_data.get("staff_id")

        try:
            staff = Staff.objects.get(staff_id=staff_id)
        except Staff.DoesNotExist:
            raise serializers.ValidationError({"error": "Staff ID does not exist"})
        first_name = staff.first_name
        last_name = staff.last_name
        email = staff.email
        username = userId(first_name.lower())

        validated_data["first_name"] = first_name
        validated_data["last_name"] = last_name
        validated_data["email"] = email
        validated_data["username"] = username
        password = validated_data.pop("password", None)
        teacher_admin = TeacherAdmin.objects.create(**validated_data)
        if password:
            teacher_admin.set_password(password)
            teacher_admin.save()
            return teacher_admin

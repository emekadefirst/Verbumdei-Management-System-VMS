from rest_framework import serializers
from .models import SubAdmin
from staff.models import Staff
from datetime import datetime


def userId(firstname):
    now = datetime.now()
    return f"{firstname}{now.strftime('%M%S')}"


class SubAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubAdmin
        fields = [
            "staff_id",
            "username",
            "password",
            "admin_id",
            "created_at",
            "first_name",
            "last_name",
            "email",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "admin_id": {"read_only": True},
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

        # Pop password from the submitted data
        password = validated_data.pop("password", None)

        # Create the SubAdmin instance
        subadmin = SubAdmin.objects.create(**validated_data)

        # Set the password if provided
        if password:
            subadmin.set_password(password)
            subadmin.save()

        return subadmin

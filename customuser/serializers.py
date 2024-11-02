import re
from .models import CustomUser
from staff.models import Staff
from parent.models import Parent
from rest_framework import serializers
from rest_framework.validators import ValidationError
from datetime import datetime


def userId(firstname):
    now = datetime.now()
    return f"{firstname}{now.strftime('%M%S')}"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id", 
            "person_id",
            "username",
            "password",
            "role",
            "created_at",
            "first_name",
            "last_name",
            "email",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "email": {"read_only": True},
            "username": {"read_only": True},
        }

    def create(self, validated_data):
        first_name = None
        last_name = None
        email = None
        username = None
        staff_id = validated_data.get("person_id")
        try:
            staff = Staff.objects.get(staff_id=staff_id)
            if staff:
                first_name = staff.first_name
                last_name = staff.last_name
                email = staff.email
                username = userId(first_name.lower())
        except Staff.DoesNotExist:
            try:
                parent = Parent.objects.get(code=self.person_id)
                self.username = userId(parent.parent_name)
            except Parent.DoesNotExist:
                raise ValueError(
                    "Invalid `person_id`: no matching `Staff` or `Parent` found"
                )

        validated_data["first_name"] = first_name
        validated_data["last_name"] = last_name
        validated_data["email"] = email
        validated_data["username"] = username
        password = validated_data.pop("password", None)
        user = CustomUser.objects.create(**validated_data)

        # Set the password if provided
        if password:
            user.set_password(password)
            user.save()

        return user

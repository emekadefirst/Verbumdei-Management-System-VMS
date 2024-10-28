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

    # def check_password(user_password):
    #     password_pattern = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
    #     return bool(re.match(password_pattern, user_password))

    # def validate_password(password):
    #     if len(password) < 8:
    #         raise ValidationError("Password must be at least 8 characters long.")
    #     if not check_password(password):
    #         raise ValidationError(
    #             "Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
    #         )

    # extra_kwargs = {
    #     "password": {"write_only": True},
    #     "created_at": {"read_only": True},
    #     "role": {"read_only": True},
    #     "email": {"read_only": True},
    #     "first_name": {"read_only": True},
    #     "last_name": {"read_only": True},
    #     "username": {"read_only": True},
    # }


def userId(firstname):
    now = datetime.now()
    return f"{firstname}{now.strftime('%M%S')}"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
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
            raise serializers.ValidationError({"error": "Staff ID does not exist"})
        

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

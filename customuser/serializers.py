from .models import CustomUser
from staff.models import Staff
from parent.models import Parent
from rest_framework import serializers
from django.contrib.auth import authenticate

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
        person_id = validated_data.get("person_id")
        password = validated_data.pop("password", None)

        if person_id and password:
            try:
                staff = Staff.objects.get(staff_id=person_id)
                username = userId(staff.first_name)
                validated_data.update({
                    "first_name": staff.first_name,
                    "last_name": staff.last_name,
                    "email": staff.email,
                    "username": username,
                })

            except Staff.DoesNotExist:
                try:
                    parent = Parent.objects.get(code=person_id)
                    validated_data.update({"username": parent.parent_name, "email": parent.email})
                except Parent.DoesNotExist:
                    raise ValidationError("Invalid `person_id`: no matching `Staff` or `Parent` found")

            user = CustomUser.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user

        raise ValidationError("Incomplete data: `person_id` and `password` are required")


class LoginSerializer(serializers.Serializer):
    person_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        person_id = data.get("person_id")
        password = data.get("password")

        if not person_id or not password:
            raise serializers.ValidationError("Both person ID and password are required.")
        user = authenticate(person_id=person_id, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials. Please try again.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        data["user"] = user
        return data

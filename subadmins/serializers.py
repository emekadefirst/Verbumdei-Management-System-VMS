from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


class SubAdminSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        user = User.objects.create(**validated_data)
        return user


class SubAdminLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user = serializers.SerializerMethodField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise ValidationError('Must include "email" and "password"')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Invalid email or password")

        if not user.check_password(password):
            raise ValidationError("Invalid email or password")

        data["user"] = user
        return data

    def get_user(self, obj):
        user = obj.get("user")
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
        }

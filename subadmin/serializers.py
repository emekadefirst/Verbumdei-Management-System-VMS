from rest_framework import serializers
from .models import SubAdmin
from staff.models import Staff


class SubAdminSerializer(serializers.ModelSerializer):
    # Use SlugRelatedField to allow lookups by 'staff_id'
    staff = serializers.SlugRelatedField(
        slug_field="staff_id", queryset=Staff.objects.all()
    )

    class Meta:
        model = SubAdmin
        fields = [
            "email",
            "username",
            "password",
            "admin_id",
            "created_at",
            "staff",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }
        read_only_fields = ("created_at", "admin_id")

    def create(self, validated_data):
        password = validated_data.pop("password")
        subadmin = SubAdmin.objects.create(**validated_data)
        subadmin.set_password(password)
        subadmin.save()

        return subadmin

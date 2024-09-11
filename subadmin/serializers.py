from rest_framework import serializers
from .models import SubAdmin
from staff.models import Staff


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["staff_id"]


class SubAdminSerializer(serializers.ModelSerializer):
    staff = StaffSerializer()

    class Meta:
        model = SubAdmin
        fields = [
            "first_name",
            "last_name",
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

    def create(self, validated_data):
        staff_data = validated_data.pop("staff")
        staff = Staff.objects.get(staff_id=staff_data["staff_id"])
        password = validated_data.pop("password")
        subadmin = SubAdmin.objects.create(staff=staff, **validated_data)
        subadmin.set_password(password)
        subadmin.save()

        return subadmin

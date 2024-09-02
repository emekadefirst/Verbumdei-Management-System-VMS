from rest_framework import serializers
from rest_framework.response import Response
from .models import Student
from grade.serializers import ClassSerializer
from parent.serializers import ParentSerializer

class StudentSerializer(serializers.ModelSerializer):
    class_assigned = ClassSerializer()
    parent = ParentSerializer()
    class Meta:
        model = Student
        fields = [
            "id",
            "first_name",
            "other_name",
            "last_name",
            "date_of_birth",
            "gender",
            "type",
            "home_address",
            "state_of_origin",
            "local_government_area",
            "nationality",
            "registration_id",
            "parent",
            "religion",
            "profile_image",
            "class_assigned",
        ]
        read_only_fields = ['registration_id', 'created_at']

    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        return student

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def get_profile_image_url(self, obj):
        request = self.context.get("request")
        if obj.profile_image and hasattr(obj.profile_image, "url"):
            return request.build_absolute_uri(obj.profile_image.url)
        return None

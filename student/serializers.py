from rest_framework import serializers
from .models import Student
from parent.models import Parent
from grade.models import Class


class StudentSerializer(serializers.ModelSerializer):
    parent = serializers.CharField()
    class_assigned = serializers.CharField()
    profile_image = serializers.ImageField()

    class Meta:
        model = Student
        fields = [
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
            "parent",
            "religion",
            "profile_image",
            "class_assigned",
        ]
        read_only_fields = ("registration_id", "created_at")

    def create(self, validated_data):
        parent_name = validated_data.pop("parent")
        class_assigned_name = validated_data.pop("class_assigned")

        # Fetch or create parent and class based on names
        parent = Parent.objects.get(
            full_name=parent_name
        )  # Adjust field name if needed
        class_assigned = Class.objects.get(
            name=class_assigned_name
        )  # Adjust field name if needed

        student = Student.objects.create(
            parent=parent, class_assigned=class_assigned, **validated_data
        )
        return student

    def update(self, instance, validated_data):
        parent_name = validated_data.pop("parent", None)
        class_assigned_name = validated_data.pop("class_assigned", None)

        if parent_name:
            parent = Parent.objects.get(full_name=parent_name)
            instance.parent = parent

        if class_assigned_name:
            class_assigned = Class.objects.get(name=class_assigned_name)
            instance.class_assigned = class_assigned

        return super().update(instance, validated_data)

    def get_profile_image_url(self, obj):
        request = self.context.get("request")
        if obj.profile_image and hasattr(obj.profile_image, "url"):
            return request.build_absolute_uri(obj.profile_image.url)
        return None

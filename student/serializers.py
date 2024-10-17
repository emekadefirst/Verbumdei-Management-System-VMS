from rest_framework import serializers
from .models import Student
from parent.models import Parent
from grade.models import Class


class StudentSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(max_length=25)

    class Meta:
        model = Student
        fields = [
            "id",
            "registration_id",  
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
            "upload",
            "img_url",
            "registration_date",
        ]
        read_only_fields = (
            "id",
            "registration_id",
            "registration_date",
            "profile_image",
        )

    def validate_parent(self, value):
        parents = Parent.objects.filter(parent_name=value)
        if parents.exists():
            if parents.count() > 1:
                raise serializers.ValidationError(
                    f"Multiple parents found with the name '{value}'."
                )
            return parents.first()  # Return the first Parent instance
        else:
            raise serializers.ValidationError(
                f"Parent with name '{value}' does not exist."
            )

    def validate_class_assigned(self, value):
        try:
            return Class.objects.get(name=value)
        except Class.DoesNotExist:
            raise serializers.ValidationError(
                f"Class with name '{value}' does not exist."
            )

    def create(self, validated_data):
        parent = validated_data.pop("parent")
        # Make sure to assign a single Parent instance
        student = Student.objects.create(
            parent=parent, **validated_data
        )
        return student

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

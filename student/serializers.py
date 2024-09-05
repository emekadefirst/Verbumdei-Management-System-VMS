from rest_framework import serializers
from .models import Student
from parent.models import Parent
from grade.models import Class


class StudentSerializer(serializers.ModelSerializer):
    parent = serializers.CharField(
        max_length=25
    ) 
    class_assigned = serializers.CharField(
        max_length=12
    ) 

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

    def validate_parent(self, value):
        try:
            return Parent.objects.get(parent_name=value)
        except Parent.DoesNotExist:
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
        class_assigned = validated_data.pop("class_assigned")
        return Student.objects.create(
            parent=parent, class_assigned=class_assigned, **validated_data
        )

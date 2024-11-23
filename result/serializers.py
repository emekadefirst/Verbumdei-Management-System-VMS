from rest_framework import serializers
from .models import Result
from student.models import Student
from grade.models import Subject, Class
from staff.models import Staff
from term.models.term import Term


class ResultSerializer(serializers.ModelSerializer):
    teacher = serializers.SlugRelatedField(
        slug_field="staff_id", queryset=Staff.objects.all()
    )
    term = serializers.SlugRelatedField(slug_field="name", queryset=Term.objects.all())
    grade = serializers.SlugRelatedField(
        slug_field="name", queryset=Class.objects.all()
    )
    student = serializers.SlugRelatedField(
        slug_field="registration_id", queryset=Student.objects.all()
    )
    subject = serializers.SlugRelatedField(
        slug_field="name", queryset=Subject.objects.all()
    )

    # Define student_full_name as a custom field
    student_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Result
        fields = [
            "id",
            "student",
            "subject",
            "grade",
            "term",
            "teacher",
            "continous_assessment",
            "examination",
            "total_marks",
            "remark",
            "created_at",
            "student_full_name",  # This will be dynamically calculated.
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "total_marks": {"read_only": True},
            "remark": {"read_only": True},
            "student_full_name": {"read_only": True},  # Make this field read-only.
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        return Result.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def get_student_full_name(self, instance):
        student = instance.student
        full_name = (
            f"{student.first_name} {student.other_name} {student.last_name}".strip()
        )
        return full_name

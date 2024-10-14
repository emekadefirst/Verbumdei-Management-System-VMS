from rest_framework import serializers
from .models import Result
from student.models import Student
from grade.models import Subject, Class
from staff.models import Staff
from term.models.term import Term
from rest_framework.exceptions import ValidationError


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ["name"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name"]


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ["name"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "other_name", "registration_id"]


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["first_name", "last_name", "other_name"]


class GetResultSerializer(serializers.ModelSerializer):
    teacher = StaffSerializer()
    term = TermSerializer()
    student = StudentSerializer()
    grade = ClassSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Result
        fields = "__all__"


class UploadSerializer(serializers.ModelSerializer):
    teacher = serializers.CharField(max_length=100)
    term = serializers.CharField(max_length=100)
    student = serializers.CharField(max_length=100)
    grade = serializers.CharField(max_length=100)
    subject = serializers.CharField(max_length=100)

    class Meta:
        model = Result
        fields = [
            "student",
            "subject",
            "grade",
            "term",
            "teacher",
            "continous_assessment",
            "examination",
        ]

    def create(self, validated_data):
        student_id = validated_data.pop("student")
        try:
            student = Student.objects.get(registration_id=student_id)
        except Student.DoesNotExist:
            raise ValidationError({"student": "Student does not exist"})

        grade_name = validated_data.pop("grade")
        try:
            grade = Class.objects.get(name=grade_name)
        except Class.DoesNotExist:
            raise ValidationError({"grade": "Grade does not exist"})

        subject_name = validated_data.pop("subject")
        try:
            subject = Subject.objects.get(name=subject_name)
        except Subject.DoesNotExist:
            raise ValidationError({"subject": "Subject does not exist"})

        term_name = validated_data.pop("term")
        try:
            term = Term.objects.get(name=term_name)
        except Term.DoesNotExist:
            raise ValidationError({"term": "Term does not exist"})

        teacher_id = validated_data.pop("teacher")
        try:
            teacher = Staff.objects.get(staff_id=teacher_id)
        except Staff.DoesNotExist:
            raise ValidationError({"teacher": "Teacher does not exist"})

        result = Result.objects.create(
            teacher=teacher,
            grade=grade,
            subject=subject,
            term=term,
            student=student,
            **validated_data
        )

        return result

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

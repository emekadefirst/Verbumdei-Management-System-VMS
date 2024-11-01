from rest_framework import serializers
from term.models.term import Term
from grade.models import Subject
from student.models import Student
from rest_framework.validators import ValidationError
from .models import Quiz, Question, Option, QuizSession, StudentResponse, Result

"""Get Serializers"""
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text"]

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)
    class Meta:
        model = Question
        fields = ["id", "text", "options"]


class QuizSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizSession
        fields = '__all__'

class StudentResponseSerializer(serializers.ModelField):
    class Meta:
        model = Result
        fields = '__all__'


class ResultSerializer(serializers.ModelField):
    class Meta:
        model = StudentResponse
        fields = "__all__"

"""Create and Update Serializer"""
class CreateQuizSerializer(serializers.ModelField):
    subject = serializers.SlugRelatedField(slug_field="name", queryset=Subject.objects.all())
    class Meta:
        model = Quiz
        fields = ["id", "type", "subject", "name", "created_at"]
        read_only_fields = ["id", "name", "created_at"]

    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class CreateQuestionSerializer(serializers.ModelSerializer):
    quiz = serializers.SlugRelatedField(slug_field="name", queryset=Quiz.objects.all())
    class Meta:
        model = Question
        fields = ["id", "quiz", "text"]

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class QuizSessionSerializer(serializers.ModelSerializer):
    term = serializers.SlugRelatedField(slug_field="name", queryset=Term.objects.all())
    quiz = serializers.SlugRelatedField(slug_field="name", queryset=Quiz.objects.all())
    students = serializers.SlugRelatedField(slug_field="registration_id", queryset=Student.objects.all())

    class Meta:
        model = QuizSession
        fields = ["id", "term", "quiz", "student", "start_time", "end_time", "code","duration", "status"]

    def create(self, validated_data):
        students = validated_data.pop("students", [])
        session = QuizSession.objects.create(**validated_data)
        if students:
            session.students.set(students)
        return session

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

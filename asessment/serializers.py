from rest_framework import serializers
from .models import Quiz, Question, Option, QuizAttempt, StudentAnswer
from grade.models import Subject


class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ["quiz_attempt", "question", "selected_option"]


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = [
            "score",
            "start_time",
            "completed_at",
            "student",
            "quiz",
            "status",
        ]
        read_only_fields = [
            "score",
            "start_time",
            "completed_at",
            "student",
            "quiz",
            "status",
        ]


class SubjectNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name"]


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "text"]


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "text", "options"]


class QuizSerializer(serializers.ModelSerializer):
    subject = SubjectNameSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["id", "type", "subject", "time_limit", "questions"]

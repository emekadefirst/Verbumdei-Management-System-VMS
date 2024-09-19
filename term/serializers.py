from rest_framework import serializers
from .models.term import Term
from .models.attendance import AttendanceReport
from student.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["registration_id"]


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'


class AttendanceReportSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    term = TermSerializer(read_only=True)
    class_assigned = serializers.CharField(read_only=True)
    teacher = serializers.CharField(read_only=True)
    total_attendance_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = AttendanceReport
        fields = [
            "id",
            "term",
            "student",
            "response",
            "attendance_count",
            "date",
            "class_assigned",
            "teacher",
            "total_attendance_count",
        ]
        read_only_fields = ["id", "date", "attendance_count"]

    def validate_response(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("Response must be a boolean value.")
        return value

    def create(self, validated_data):
        student_id = self.context["request"].data.get("student")
        term_id = self.context["request"].data.get("term")

        try:
            student = Student.objects.get(registration_id=student_id)
            term = Term.objects.get(id=term_id)
        except Student.DoesNotExist:
            raise serializers.ValidationError(
                "Student with this registration ID does not exist."
            )
        except Term.DoesNotExist:
            raise serializers.ValidationError("Term with this ID does not exist.")

        attendance_report = AttendanceReport.objects.create(
            student=student, term=term, **validated_data
        )
        return attendance_report

    def update(self, instance, validated_data):
        if (
            "response" in validated_data
            and validated_data["response"] != instance.response
        ):
            instance.response = validated_data["response"]
            if instance.response:
                instance.increment_attendance()
            else:
                # If changing from present to absent, decrement the count
                instance.attendance_count = max(1, instance.attendance_count - 1)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["student"] = StudentSerializer(instance.student).data
        representation["term"] = TermSerializer(instance.term).data
        return representation

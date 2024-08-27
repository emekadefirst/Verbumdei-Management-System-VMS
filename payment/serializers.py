from rest_framework import serializers
from student.models import Student
from .models import Payment, PaymentType
from student.serializers import StudentSerializer


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = "__all__"

    def create(self, validated_data):
        parent = PaymentType.objects.create(**validated_data)
        return parent

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PaymentSerializers(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer()
    student = StudentSerializer()

    class Meta:
        model = Payment
        fields = [
            "id",
            "payment_type",
            "student",
            "method",
            "status",
            "reference",
            "created_at",
        ]

    def create(self, validated_data):
        reference = validated_data.pop("reference", None)
        payment_type_data = validated_data.pop("payment_type")
        student_data = validated_data.pop("student")

        payment_type = PaymentType.objects.get(**payment_type_data)
        student = Student.objects.get(**student_data)

        payment = Payment.objects.create(
            payment_type=payment_type,
            student=student,
            reference=reference,
            **validated_data
        )
        return payment

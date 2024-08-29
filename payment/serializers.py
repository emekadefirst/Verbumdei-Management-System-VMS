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
    class Meta:
        model = Payment
        fields = [
            "parent",
            "payment_type",
            "student",
            "method",
            "created_at",
            "cost",  # Include cost field here
        ]

    def create(self, validated_data):
        payment_type = validated_data.get("payment_type")
        student = validated_data.get("student")
        method = validated_data.get("method")
        cost = payment_type.cost
        payment = Payment.objects.create(
            payment_type=payment_type,
            student=student,
            method=method,
            cost=cost,  # Save the cost here
        )

        return payment

    def update(self, instance, validated_data):
        instance.payment_type = validated_data.get(
            "payment_type", instance.payment_type
        )
        instance.student = validated_data.get("student", instance.student)
        instance.method = validated_data.get("method", instance.method)
        if "payment_type" in validated_data:
            instance.cost = instance.payment_type.cost

        instance.save()
        return instance

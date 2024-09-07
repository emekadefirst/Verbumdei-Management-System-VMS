from rest_framework import serializers
from student.models import Student
from parent.models import Parent
from parent.serializers import ParentSerializer
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
    parent = serializers.SlugRelatedField(slug_field="code", queryset=Parent.objects.all())
    payment_type = serializers.SlugRelatedField(slug_field="name", queryset=PaymentType.objects.all())
    student = serializers.SlugRelatedField(slug_field="registration_id", queryset=Student.objects.all())
    class Meta:
        model = Payment
        fields = ["parent", "payment_type", "student", "method"]
        extra_kwargs = {
            "method": {
                "error_messages": {"invalid_choice": '"Online" is not a valid choice.'}
            }
        }

    def create(self, validated_data):
        parent = validated_data.get("parent")
        payment_type = validated_data.get("payment_type")
        student = validated_data.get("student")
        method = validated_data.get("method")

        # Optionally, generate a unique reference if not provided
        reference = validated_data.get("reference", None)
        if not reference:
            reference = f"{parent.code}-{student.registration_id}-{payment_type.name}"

        payment = Payment.objects.create(
            parent=parent,
            payment_type=payment_type,
            student=student,
            method=method,
            reference=reference,
        )
        return payment

    def update(self, instance, validated_data):
        instance.parent = validated_data.get("parent", instance.parent)
        instance.payment_type = validated_data.get(
            "payment_type", instance.payment_type
        )
        instance.student = validated_data.get("student", instance.student)
        instance.method = validated_data.get("method", instance.method)
        instance.status = validated_data.get("status", instance.status)
        # Optionally update the reference if needed
        reference = validated_data.get("reference", None)
        if reference:
            instance.reference = reference

        instance.save()
        return instance

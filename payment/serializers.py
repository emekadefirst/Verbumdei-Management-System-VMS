from rest_framework import serializers
from .models import Payment, PaymentType
from student.serializers import StudentSerializer

class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        field = '__all__'

    def create(self, validated_data):
        parent = PaymentType.objects.create(**validated_data)
        return parent

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PaymentSerializers(serializers.ModelSerializer):
    payment_type = PaymentTypeSerializer()
    student = PaymentTypeSerializer()
    class Meta:
        model = PaymentType
        field = ["id", "payment_type", "student", "method", "status", 'created_at']

    def create(self, validated_data):
        parent = Payment.objects.create(**validated_data)
        return parent

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

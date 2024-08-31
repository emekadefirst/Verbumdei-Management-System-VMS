from rest_framework import serializers
from .models import Parent

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = [
            "email" "phone_number_1",
            "phone_number_2",
            "parent_name",
            "home_address",
        ]

    def create(self, validated_data):
        parent = Parent.objects.create(**validated_data)
        return parent

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

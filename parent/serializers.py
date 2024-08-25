from rest_framework import serializers
from .models import Parent

class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        field = '__all__'
        
    def create(self, validated_data):
        parent = Parent.objects.create(**validated_data)
        return parent

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
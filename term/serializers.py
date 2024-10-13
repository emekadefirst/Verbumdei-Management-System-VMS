from rest_framework import serializers
from .models.term import Term


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = '__all__'
        
    def create(self, validated_data):
        term = Term.objects.create(**validated_data)
        return term
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
        
        




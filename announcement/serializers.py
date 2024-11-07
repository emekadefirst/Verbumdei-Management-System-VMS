from rest_framework import serializers
from .models import Annoucement

class AnnoucementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annoucement
        fields = ['id', 'title', 'content', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data, *args, **kwargs):
        return Annoucement.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

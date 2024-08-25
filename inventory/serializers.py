from rest_framework import serializers
from .models import Inventory, InventoryType


class InventoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryType
        field = '__all__'
        
class InventorySerializer(serializers.ModelSerializer):
    type = InventoryTypeSerializer()
    class Meta:
        model = Inventory
        field = ['name', 'type', 'quantity', 'time_of_purchase']
        
    def create(self, validated_data):
        inventory = Inventory.objects.create(**validated_data)
        return inventory

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

        
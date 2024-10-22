from rest_framework import serializers
from .models import Inventory, InventoryType


class InventoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryType
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(
        slug_field="name", queryset=InventoryType.objects.all()
    )

    class Meta:
        model = Inventory
        fields = ["name", "type", "quantity", "unit_cost", "total_cost"]
        read_only_fields = ("id", "time_of_purchase", "total_cost")

    def create(self, validated_data):
        inventory = Inventory.objects.create(**validated_data)
        return inventory


    def update(self, instance, validated_data):
        # Update each field of the instance with the validated data
        instance.type = validated_data.get("type", instance.type)
        instance.name = validated_data.get("name", instance.name)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.unit_cost = validated_data.get("unit_cost", instance.unit_cost)

        # Save the instance to persist changes to the database
        instance.save()

        return instance

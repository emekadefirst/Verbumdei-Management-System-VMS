from rest_framework import serializers
from .models import Inventory, InventoryType


class InventoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryType
        fields = '__all__'

class InventorySerializer(serializers.ModelSerializer):
    type = InventoryTypeSerializer('type')
    fields = ['name', 'type', 'quantity', 'unit_cost']
    read_only_fields = ('id', 'time_of_purchase', 'total_cost')

    def create(self, validated_data):
        inventory = Inventory.objects.create(**validated_data)
        return inventory

    def update(self, instance, validated_data):
        from rest_framework import serializers


from .models import Inventory, InventoryType


class InventoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryType
        fields = "__all__"


class InventorySerializer(serializers.ModelSerializer):
    type = serializers.CharField(write_only=True)
    type_details = InventoryTypeSerializer(source="type", read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "name",
            "type",
            "type_details",
            "quantity",
            "unit_cost",
            "total_cost",
            "time_of_purchase",
        ]
        read_only_fields = ["id", "time_of_purchase", "total_cost"]

    def create(self, validated_data):
        type_name = validated_data.pop("type")
        inventory_type, _ = InventoryType.objects.get_or_create(name=type_name)
        inventory = Inventory.objects.create(type=inventory_type, **validated_data)
        return inventory

    def update(self, instance, validated_data):
        if "type" in validated_data:
            type_name = validated_data.pop("type")
            inventory_type, _ = InventoryType.objects.get_or_create(name=type_name)
            instance.type = inventory_type
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["type"] = representation["type_details"]["name"]
        del representation["type_details"]
        return representation
        return super().update(instance, validated_data)

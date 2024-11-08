from rest_framework import serializers
from .models  import InventoryType, Inventory, Voucher


class VourcherSerializers(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field="name", queryset=InventoryType.objects.all())
    class Meta:
        model = Voucher
        fields = ["id", "type", "name", "quantity", "unit_cost", "code", "status", "created_at"]
        read_only_fields = ["id", "created_at", "code"]

    def create(self, validated_data, *args, **kwargs):
        return Voucher.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

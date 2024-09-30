from .models import Bus
from staff.models import Staff
from rest_framework import serializers


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["staff_id"]

    def validate_staff_id(self, value):
        try:
            staff_data = Staff.objects.get(staff_id=value)
        except Staff.DoesNotExist:
            raise serializers.ValidationError("Staff with this ID does not exist.")
        if staff_data.staff_type != "NON_TEACHING":
            raise serializers.ValidationError(
                "Only non-teaching staff are allowed to be bus drivers."
            )
        return value


class BusSerializer(serializers.ModelSerializer):
    # Reference to the driver's staff ID for creating and updating
    driver = serializers.PrimaryKeyRelatedField(
        queryset=Staff.objects.filter(staff_type="NON_TEACHING"),
        source="driver_name",  # maps to driver_name in Bus model
        write_only=True,
    )

    # Display the staff ID in responses
    driver_name = serializers.CharField(source="driver_name.staff_id", read_only=True)

    class Meta:
        model = Bus
        fields = [
            "id",
            "plate_number",
            "manufacturer",
            "model",
            "year",
            "color",
            "sit_capacity",
            "driver",  # for input
            "driver_name",  # for output
            "created_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        # Handles the creation of a Bus instance
        return Bus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update the instance fields
        instance.plate_number = validated_data.get(
            "plate_number", instance.plate_number
        )
        instance.manufacturer = validated_data.get(
            "manufacturer", instance.manufacturer
        )
        instance.model = validated_data.get("model", instance.model)
        instance.year = validated_data.get("year", instance.year)
        instance.color = validated_data.get("color", instance.color)
        instance.sit_capacity = validated_data.get(
            "sit_capacity", instance.sit_capacity
        )
        instance.driver_name = validated_data.get("driver_name", instance.driver_name)
        instance.save()
        return instance

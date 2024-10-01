from .models import Bus
from staff.models import Staff
from rest_framework import serializers


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["staff_id", "first_name", "last_name"]

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
    driver = serializers.CharField(source="driver.staff_id")
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
            "driver", 
            "created_at",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }

    def create(self, validated_data):
        driver_staff_id = validated_data.pop('driver')['staff_id']
        try:
            driver = Staff.objects.get(staff_id=driver_staff_id)
        except Staff.DoesNotExist:
            raise serializers.ValidationError(f"Staff with ID {driver_staff_id} does not exist.")
        bus = Bus.objects.create(driver=driver, **validated_data)
        return bus

    def update(self, instance, validated_data):
        if 'driver' in validated_data:
            driver_staff_id = validated_data.pop('driver')['staff_id']
            try:
                driver = Staff.objects.get(staff_id=driver_staff_id)
            except Staff.DoesNotExist:
                raise serializers.ValidationError(f"Staff with ID {driver_staff_id} does not exist.")
            instance.driver = driver
        return super().update(instance, validated_data)


class GetBusSerializer(serializers.ModelSerializer):
    driver = StaffSerializer()

    class Meta:
        model = Bus
        fields = '__all__'

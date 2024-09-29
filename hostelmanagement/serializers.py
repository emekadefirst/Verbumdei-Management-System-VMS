from staff.models import Staff
from .models import Hostel, Room
from student.models import Student
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
            raise serializers.ValidationError("Only non-teaching staff are allowed.")
        return value


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["registration_id"]

    def validate_registration_id(self, value):
        try:
            student_data = Student.objects.get(registration_id=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student with this ID does not exist.")

        if student_data.type != "BOARDER":
            raise serializers.ValidationError("Only Boarders are allowed.")

        return value


class HostelSerializer(serializers.ModelSerializer):
    warden = serializers.CharField(source="warden.staff_id")

    class Meta:
        model = Hostel
        fields = ["type", "warden"]

    def create(self, validated_data):
        warden_id = validated_data.pop("warden")
        warden = Staff.objects.get(staff_id=warden_id)
        return Hostel.objects.create(warden=warden, **validated_data)

    def update(self, instance, validated_data):
        warden_id = validated_data.get("warden")
        if warden_id:
            instance.warden = Staff.objects.get(staff_id=warden_id)

        instance.type = validated_data.get("type", instance.type)
        instance.save()
        return instance


class RoomSerializer(serializers.ModelSerializer):
    occupants = StudentSerializer(many=True, read_only=True)
    class Meta:
        model = Room
        fields = [
            "id",
            "room_id",
            "max_occupants",
            "occupants",
            "current_occupants",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "current_occupants": {"read_only": True},
        }

    def create(self, validated_data):
            occupants_ids = validated_data.pop("occupants")
            room = Room.objects.create(**validated_data)
            for occupant_id in occupants_ids:
                student = Student.objects.get(registration_id=occupant_id)
                room.occupants.add(student)
            return room

    def update(self, instance, validated_data):
        occupants_data = validated_data.pop("occupants", None)
        instance.room_id = validated_data.get("room_id", instance.room_id)
        instance.max_occupants = validated_data.get("max_occupants", instance.max_occupants)

        if occupants_data:
            instance.occupants.clear()
            for occupant_id in occupants_data:
                student = Student.objects.get(registration_id=occupant_id)
                instance.occupants.add(student)

        instance.save()
        return instance
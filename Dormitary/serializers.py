from staff.models import Staff
from .models import Hostel, Dorm
from student.models import Student
from rest_framework import serializers
from rest_framework.validators import ValidationError


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
            raise serializers.ValidationError("Only non-teaching staff are allowed.")
        return value


class HostelSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=["MALE", "FEMALE"])
    warden = serializers.CharField(max_length=25)

    class Meta:
        model = Hostel
        fields = ["id", "type", "warden"]
        read_only = ["id"]

    def create(self, validated_data):
        type = validated_data["type"]
        warden_id = validated_data["warden"]
        warden = Staff.objects.get(staff_id=warden_id)

        if warden:
            hostel = Hostel.objects.create(type=type, warden=warden)
            return hostel
        raise serializers.ValidationError("Invalid warden.")

    def update(self, instance, validated_data):
        instance.type = validated_data.get("type", instance.type)
        warden_id = validated_data.get("warden", instance.warden.staff_id)
        warden = Staff.objects.get(staff_id=warden_id)
        if warden:
            instance.warden = warden
            instance.save()
        else:
            raise serializers.ValidationError("Invalid warden.")

        return instance


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["registration_id", "first_name", "last_name"]

    def validate_registration_id(self, value):
        try:
            student_data = Student.objects.get(registration_id=value)
        except Student.DoesNotExist:
            raise serializers.ValidationError("Student with this ID does not exist.")

        if student_data.type != "BOARDER":
            raise serializers.ValidationError("Only Boarders are allowed.")

        return value


class DormSerializer(serializers.ModelSerializer):
    hostel = serializers.PrimaryKeyRelatedField(
        queryset=Hostel.objects.all()
    )  
    occupants = StudentSerializer(many=True)

    class Meta:
        model = Dorm
        fields = ["id", "hostel", "dorm_code", "max_occupants", "occupants", "is_full"]
        read_only = ["id", "dorm_code", "is_full"]

    def create(self, validated_data):
        occupants_data = validated_data.pop("occupants", [])
        hostel_type = validated_data.pop("hostel")

        # Look up the Hostel objects based on the type
        hostels = Hostel.objects.filter(type=hostel_type)
        if not hostels.exists():
            raise serializers.ValidationError(f"No hostel of type '{hostel_type}' exists.")
        elif hostels.count() > 1:
            raise serializers.ValidationError(f"Multiple hostels found for type '{hostel_type}'. Please specify further.")

        dorm = Dorm.objects.create(hostel=hostels.first(), **validated_data)

        if len(occupants_data) > dorm.max_occupants:
            raise serializers.ValidationError(f"{dorm.dorm_code} cannot accommodate more than {dorm.max_occupants} occupants.")

        for occupant_data in occupants_data:
            student = Student.objects.get(registration_id=occupant_data["registration_id"])
            if student.gender != dorm.hostel.type:
                raise serializers.ValidationError(f"Cannot assign {student.first_name} to {dorm.hostel.type} hostel.")
            dorm.occupants.add(student)

        return dorm  # Return the created dorm instance

    def update(self, instance, validated_data):
        occupants_data = validated_data.pop("occupants", None)

        # Update the Dorm fields
        instance.hostel = validated_data.get("hostel", instance.hostel)
        instance.max_occupants = validated_data.get(
            "max_occupants", instance.max_occupants
        )
        instance.save()

        # Clear current occupants and add new ones
        if occupants_data is not None:
            instance.occupants.clear()  # Clear current occupants
            for occupant_data in occupants_data:
                student = Student.objects.get(
                    registration_id=occupant_data["registration_id"]
                )
                instance.occupants.add(student)

        return instance


class GetDormSerializer(serializers.ModelSerializer):
    hostel = HostelSerializer(read_only=True) 
    occupants = StudentSerializer(
        many=True, read_only=True
    )  # Serialize occupants as a list of students

    class Meta:
        model = Dorm
        fields = ["id", "hostel", "dorm_code", "max_occupants", "occupants", "is_full"]

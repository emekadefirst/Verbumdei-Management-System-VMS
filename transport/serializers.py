from staff.models import Staff
from .models import Bus, Commute
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


class BusSerializer(serializers.ModelSerializer):
    driver = StaffSerializer()
    class Meta:
        model = Bus
        fields = ["plate_number", "driver"]


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["registration_id", "first_name", "last_name"] 


class CommuteSerializer(serializers.ModelSerializer):
    bus = serializers.CharField(write_only=True)
    students = serializers.CharField(write_only=True)

    bus_details = BusSerializer(source="bus", read_only=True)
    student_details = StudentSerializer(source="students", many=True, read_only=True)

    class Meta:
        model = Commute
        fields = ["bus", "students", "bus_details", "student_details"]

    def create(self, validated_data):
        bus_plate_number = validated_data.pop("bus")
        student_id = validated_data.pop("students")
        try:
            bus = Bus.objects.get(plate_number=bus_plate_number)
        except Bus.DoesNotExist:
            raise serializers.ValidationError(
                f"Bus with plate number {bus_plate_number} does not exist."
            )
        try:
            student = Student.objects.get(registration_id=student_id)
        except Student.DoesNotExist:
            raise serializers.ValidationError(
                f"Student with registration ID {student_id} does not exist."
            )

        commute = Commute.objects.create(bus=bus, **validated_data)
        commute.students.set([student])

        return commute


    def update(self, instance, validated_data):
        if "bus" in validated_data:
            bus_plate_number = validated_data.pop("bus")
            try:
                new_bus = Bus.objects.get(plate_number=bus_plate_number)
                instance.bus = new_bus
            except Bus.DoesNotExist:
                raise serializers.ValidationError(
                    f"Bus with plate number {bus_plate_number} does not exist."
                )

        if "students" in validated_data:
            student_id = validated_data.pop("students")
            try:
                student = Student.objects.get(registration_id=student_id)
                if instance.is_full:
                    raise serializers.ValidationError(
                        f"The bus {instance.bus.plate_number} is full."
                    )
                instance.add_student(student)
            except Student.DoesNotExist:
                raise serializers.ValidationError(
                    f"Student with registration ID {student_id} does not exist."
                )
            except ValidationError as e:
                raise serializers.ValidationError(str(e))

        instance.save()
        return instance


class GetCommuteSerializer(serializers.ModelSerializer):
    bus = BusSerializer()
    students = StudentSerializer(many=True)
    is_full = serializers.BooleanField()  
    class Meta:
        model = Commute
        fields = ["id", "uuid", "bus", "students", "is_full"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["students_count"] = instance.students.count()
        return representation

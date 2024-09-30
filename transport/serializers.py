from staff.models import Staff
from .models import Bus, Commute
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

class CommuteSerializer(serializers.ModelSerializer):
    bus = serializers.CharField(source="bus.plate_number", read_only=True) 
    bus_id = serializers.PrimaryKeyRelatedField(queryset=Bus.objects.all(), source="bus")  
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True) 
    is_full = serializers.ReadOnlyField()  
    class Meta:
        model = Commute
        fields = ["uuid", "bus", "bus_id", "students", "is_full"]

    def create(self, validated_data):
        parent = Commute.objects.create(**validated_data)
        return parent

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    # def validate_students(self, value):
    #     """
    #     Check if bus is not full before adding more students.
    #     """
    #     bus = self.instance.bus if self.instance else self.initial_data.get("bus")
    #     if bus.sit_capacity < len(value):
    #         raise serializers.ValidationError(
    #             f"The bus with plate number {bus.plate_number} has reached full capacity."
    #         )
    #     return value

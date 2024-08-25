from rest_framework import serializers
from .models import Student
 
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'other_name', 'last_name', 'date_of_birth', 'gender', 'type', 'home_address', 'state_of_origin', 'local_government_area', 'nationality', 'parent', 'religion', 'profile_image', 'class_assigned' ] 
        read_only_fields = ['registration_id', 'created_at']
        
    
    def create(self, validated_data):
        student = Student.objects.create(**validated_data)
        return student
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
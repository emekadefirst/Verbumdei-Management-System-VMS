from rest_framework import serializers
from .models import Class, Subject, SubjectMaterial
from staff.serializers import StaffSerializer

class SubjectMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectMaterial
        fields = ['id', 'subject', 'material', 'created_at']

class ClassSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    teacher = StaffSerializer(read_only=True)

    class Meta:
        model = Class
        fields = ['id', 'name', 'teacher', 'subjects', 'created_at']

class SubjectSerializer(serializers.ModelSerializer):
    study_materials = SubjectMaterialSerializer(many=True, read_only=True)
    teacher = StaffSerializer(read_only=True)
    grade = ClassSerializer(read_only=True)  # Nesting ClassSerializer

    class Meta:
        model = Subject
        fields = ['id', 'name', 'grade', 'teacher', 'study_materials', 'created_at']

# If you want to create or update models through the API, you may need to handle nested writes.
class SubjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'grade', 'teacher']

    def validate_teacher(self, value):
        if value.staff_type != 'TEACHING':
            raise serializers.ValidationError(f'Teacher {value} is not a teaching staff member.')
        return value

class ClassCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name', 'teacher']

    def validate_teacher(self, value):
        if value.staff_type != 'TEACHING':
            raise serializers.ValidationError(f'Teacher {value} is not a teaching staff member.')
        return value

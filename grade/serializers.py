from rest_framework import serializers
from .models import Class, Subject, SubjectMaterial
from student.models import Student
from staff.models import Staff


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["id","first_name", "last_name", "img_url", "staff_id"]


class SubjectMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectMaterial
        fields = ['id', 'subject', 'material', 'created_at']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "first_name", "last_name","registration_id", "img_url"]


class ClassSerializer(serializers.ModelSerializer):
    teacher = StaffSerializer(read_only=True)
    students = StudentSerializer(
        many=True, read_only=True
    )  

    class Meta:
        model = Class
        fields = ["id", "name", "teacher", "students", "student_count", "created_at"]


class SubjectSerializer(serializers.ModelSerializer):
    study_materials = SubjectMaterialSerializer(many=True, read_only=True)
    teacher = StaffSerializer(read_only=True)
    grade = ClassSerializer(read_only=True)  

    class Meta:
        model = Subject
        fields = ['id', 'name', 'grade', 'teacher', 'study_materials', 'created_at']


class SubjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'grade', 'teacher']

    def validate_teacher(self, value):
        if value.staff_type != 'TEACHING':
            raise serializers.ValidationError(f'Teacher {value} is not a teaching staff member.')
        return value


class ClassCreateUpdateSerializer(serializers.ModelSerializer):
    students = serializers.SlugRelatedField(
        many=True,
        slug_field='registration_id', 
        queryset=Student.objects.all(),
        required=False  
    )

    class Meta:
        model = Class
        fields = ['id', 'name', 'teacher', 'students']

    def validate_teacher(self, value):
        if value.staff_type != 'TEACHING':
            raise serializers.ValidationError(f'Teacher {value} is not a teaching staff member.')
        return value

    def create(self, validated_data):
        students = validated_data.pop('students', [])
        class_instance = Class.objects.create(**validated_data)
        if students:
            class_instance.students.set(students)
        return class_instance

    def update(self, instance, validated_data):
        students = validated_data.pop('students', None)
        instance.name = validated_data.get('name', instance.name)
        instance.teacher = validated_data.get('teacher', instance.teacher)
        instance.save()
        if students is not None:
            instance.students.set(students)

        return instance

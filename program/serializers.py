from rest_framework import serializers
from .models import Event, Exam, Mid_Exam

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'date']
        readonly = ['created_at']
        
class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['name', 'start_date', 'end_date']
        readonly = ['created_at']
    
class MidExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mid_Exam
        fields = ['name', 'start_date', 'end_date']
        readonly = ['created_at']
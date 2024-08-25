from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event, Exam, Mid_Exam
from .serializers import EventSerializer, ExamSerializer, MidExamSerializer

class EventView(APIView):
    def get(self, request, format=None):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailView(APIView):
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        exam = self.get_object(pk)
        serializer = EventSerializer(exam)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExamView(APIView):
    def get(self, request, format=None):
        exam = Exam.objects.all()
        serializer = ExamSerializer(exam, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExamDetailView(APIView):
    def get_object(self, pk):
        try:
            return Exam.objects.get(pk=pk)
        except Exam.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        exam = self.get_object(pk)
        serializer = ExamSerializer(exam)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        exam = self.get_object(pk)
        serializer = ExamSerializer(exam, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MidExamView(APIView):
    def get(self, request, format=None):
        mid = Mid_Exam.objects.all()
        serializer = MidExamSerializer(mid, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = MidExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MidExamDetailView(APIView):
    def get_object(self, pk):
        try:
            return Mid_Exam.objects.get(pk=pk)
        except Mid_Exam.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        mid = self.get_object(pk)
        serializer = MidExamDetailView(mid)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        mid = self.get_object(pk)
        serializer = MidExamDetailView(mid, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



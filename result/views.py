from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Result
from student.models import Student
from .serializers import GetResultSerializer, UploadSerializer


class AllResultView(APIView):
    def get(self, request):
        obj = Result.objects.all() 
        serializer = GetResultSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadResultView(APIView):
    def post(self, request):
        serializer = UploadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResultDetailView(APIView):
    def get_object(self, pk):
        try:
            return Result.objects.get(pk=pk)
        except Result.DoesNotExist:
            raise NotFound(detail="Result not found")  # Raise NotFound exception

    def get(self, request, pk):
        result = self.get_object(pk)
        serializer = GetResultSerializer(result)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        result = self.get_object(pk)
        serializer = GetResultSerializer(result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentResultHistoryView(APIView):
    def get(self, request, student_id):
        try:
            student = Student.objects.get(registration_id=student_id)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        results = Result.objects.filter(student=student)  # Filter by the student instance
        serializer = GetResultSerializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StudentRecentResult(APIView):
    def post(self, request):
        serializer = GetResultSerializer(results, many=True)
        term_name= serializer.data.get('term_name')
        student_id = serializer.data.get('student_id')
        try:
            student = Student.objects.get(registration_id=student_id)
        except Student.DoesNotExist:
            return Response({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        results = Result.objects.filter(student=student_id, term__name=term_name)  
        if results.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "No results found for the given student and term"}, status=status.HTTP_404_NOT_FOUND)

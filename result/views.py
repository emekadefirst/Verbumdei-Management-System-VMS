from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Result
from student.models import Student
from .serializers import ResultSerializer

class AllResultView(APIView):
    def get(self, request):
        results = Result.objects.all()
        serializer = ResultSerializer(results, many=True)
        data = serializer.data
        return Response(data, status=status.HTTP_200_OK)


class UploadResultView(APIView):
    def post(self, request):
        serializer = ResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateResultView(APIView):
    def get_object(self, pk):
        try:
            return Result.objects.get(pk=pk)
        except Result.DoesNotExist:
            raise NotFound(detail="Result not found")  
    def put(self, request, pk):
        result = self.get_object(pk)
        serializer = ResultSerializer(result, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentResultHistoryView(APIView):
    def get(self, request, student_id):
        results = Result.objects.filter(student__registration_id=student_id)
        if results.exists():
            serializer = ResultSerializer(results, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Result not found."}, status=status.HTTP_404_NOT_FOUND)


class GetStudentResult(APIView):
    def get(self, request, registration_id):
        term = request.GET.get('term', None)
        if term is None:
            return Response({"detail": "Term is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            results = Result.objects.filter(student__registration_id=registration_id, term__name=term)
            if not results.exists():
                return Response({"detail": "No result found for this student in this term."}, status=status.HTTP_404_NOT_FOUND)
            serializer = ResultSerializer(results, many=True)  
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Result.DoesNotExist:
            return Response({"detail": "Term not found."}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.response import Response
from rest_framework.decorators import action
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from django.db.models import Q
from django.db.models.functions import Lower
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class StudentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        student = Student.objects.all()
        serializer = StudentSerializer(student, many=True, context={"request": request})
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        student = self.get_object(pk)
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentCountView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        count = Student.objects.count()
        return Response({"count": count})


class StudentSearch(APIView):
    def post(self, request):
        search_query = request.data.get("query", "")
        if search_query:
            search_results = Student.objects.filter(
                Q(name__icontains=search_query)
                | Q(registration_id__icontains=search_query)
                | Q(first_name__icontains=search_query)
                | Q(other_name__icontains=search_query)
                | Q(last_name__icontains=search_query)
            )

            search_results = search_results.order_by("registration_id")
            serializer = StudentSerializer(search_results, many=True)
            return Response(serializer.data)
        else:
            return Response("Invalid search query", status=status.HTTP_400_BAD_REQUEST)


class StudentByParent(APIView):
    def get(self, request, parent_id: int):
        students = Student.objects.filter(parent=parent_id)
        if not students.exists():
            return Response({"detail": "No students found for this parent code."}, status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
from django.http import Http404
from .models import Parent
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ParentSerializer
from student.models import Student
from student.serializers import StudentSerializer


class ParentView(APIView):
    def get(self, request, format=None):
        parnet = Parent.objects.all()
        serializer = ParentSerializer(parnet, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParentDetailView(APIView):
    def get_object(self, pk):
        try:
            return Parent.objects.get(pk=pk)
        except Parent.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        parent = self.get_object(pk)
        serializer = ParentSerializer(parent)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        parent = self.get_object(pk)
        serializer = ParentSerializer(parent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        parent = self.get_object(pk)
        parent.delete()


class ParentCountView(APIView):
    def get(self, request, format=None):
        count = Parent.objects.count()
        return Response({"count": count})


class ParentDashboard(APIView):
    def get(self, request, code: str):
        try:
            parent = Parent.objects.get(
                code=code
            )
            parent_name = parent.parent_name
        except Parent.DoesNotExist:
            return Response(
                {"error": "Parent not found."}, status=status.HTTP_404_NOT_FOUND
            )

        related_students = Student.objects.filter(parent=parent)
        parent_serializer = ParentSerializer(parent)
        students_serializer = StudentSerializer(related_students, many=True)
        user_data = parent_serializer.data
        user_data["ward(s)"] = students_serializer.data

        return Response(
            {"parent": user_data},
            status=status.HTTP_200_OK,
        )

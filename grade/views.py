from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Class, Subject, SubjectMaterial
from .serializers import (
    ClassSerializer, ClassCreateUpdateSerializer,
    SubjectSerializer, SubjectCreateUpdateSerializer,
    SubjectMaterialSerializer
)

class ClassListCreateAPIView(APIView):
    def get(self, request):
        classes = Class.objects.all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClassCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ClassRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, pk):
        class_instance = get_object_or_404(Class, pk=pk)
        serializer = ClassSerializer(class_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        class_instance = get_object_or_404(Class, pk=pk)
        serializer = ClassCreateUpdateSerializer(class_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        class_instance = get_object_or_404(Class, pk=pk)
        class_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubjectListCreateAPIView(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubjectCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(subject)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectCreateUpdateSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subject = get_object_or_404(Subject, pk=pk)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SubjectMaterialListCreateAPIView(APIView):
    def get(self, request):
        subject_materials = SubjectMaterial.objects.all()
        serializer = SubjectMaterialSerializer(subject_materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SubjectMaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SubjectMaterialRetrieveUpdateDestroyAPIView(APIView):
    def get(self, request, pk):
        subject_material = get_object_or_404(SubjectMaterial, pk=pk)
        serializer = SubjectMaterialSerializer(subject_material)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        subject_material = get_object_or_404(SubjectMaterial, pk=pk)
        serializer = SubjectMaterialSerializer(subject_material, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



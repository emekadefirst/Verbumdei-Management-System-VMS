from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *


class QuizView(APIView):
    def post(self, request, format=None):
        serializer = CreateQuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        obj = Quiz.objects.all()
        serializer = QuizSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionView(APIView):
    def post(self, request, format=None):
        serializer = CreateQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        obj = Quiz.objects.all()
        serializer = QuestionSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

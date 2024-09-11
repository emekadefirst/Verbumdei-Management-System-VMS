from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Quiz, Question, Option, QuizAttempt, StudentAnswer
from .serializers import QuizSerializer, QuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Quiz, QuizAttempt, Question, Option, StudentAnswer
from .serializers import QuizSerializer, StudentAnswerSerializer, QuizAttemptSerializer
from student.models import Student   

"""Quiz view"""
class QuizView(APIView):
    def get(self, request):
        data = Quiz.objects.all()
        serializers = QuizSerializer(data, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDetailView(APIView):
    def get_object(self, pk):
        try:
            return Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        quiz = self.get_object(pk)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        quiz = self.get_object(pk)
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionView(APIView):
    def post(self, request, formart=None):
        serializers = QuestionSerializer()
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def get (self, request, *args, **kwargs):
        data = Question.objects.all()
        serializers = QuestionSerializer(data, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class QuestionDetailView(APIView):
    def get_object(self, pk):
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SubmitQuizView(APIView):
    def post(self, request, registration_id):
        student = Student.objects.get(registration_id=registration_id)
        quiz_name = request.data.get("quiz_subject")
        quiz = get_object_or_404(Quiz, name=quiz_name)
        quiz_attempt = QuizAttempt.objects.create(student=student, quiz=quiz)
        answers = request.data.get("answers", [])
        for answer_data in answers:
            question_id = answer_data.get("question")
            selected_option_id = answer_data.get("selected_option")
            question = get_object_or_404(Question, id=question_id, quiz=quiz)
            selected_option = get_object_or_404(
                Option, id=selected_option_id, question=question
            )

            StudentAnswer.objects.create(
                quiz_attempt=quiz_attempt,
                question=question,
                selected_option=selected_option,
            )

        result = quiz_attempt.calculate_score()

        return Response(
            {
                "message": "Quiz submitted successfully.",
                "score": result["score"],
                "total": result["total"],
                "percentage": result["percentage"],
            },
            status=status.HTTP_200_OK,
        )

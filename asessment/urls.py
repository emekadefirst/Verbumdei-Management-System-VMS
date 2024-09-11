from django.urls import path
from .views import *

urlpatterns = [
    path("", QuizView.as_view(), name="parent"),
    path("<int:pk>/", QuizDetailView.as_view(), name="parent_detail"),
    path("question/", QuestionView.as_view(), name="question"),
    path("question/<int:pk>/", QuestionDetailView.as_view(), name="question_detail"),
    path("student-answer/", SubmitQuizView.as_view(), name="submit_answer"),
]

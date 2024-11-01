from django.urls import path
from .import views

urlpatterns = [
    path("quiz/", views.QuizView.as_view(), name="quiz"),
    path("questions/", views.QuizView.as_view(), name="question"),
]

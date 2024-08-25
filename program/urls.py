from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.EventView.as_view(), name='event-list'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('exams/', views.ExamView.as_view(), name='exam-list'),
    path('exams/<int:pk>/', views.ExamDetailView.as_view(), name='exam-detail'),
    path('mid-exams/', views.MidExamView.as_view(), name='mid-exam-list'),
    path('mid-exams/<int:pk>/', views.MidExamDetailView.as_view(), name='mid-exam-detail'),
]

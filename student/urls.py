from django.urls import path
from . import views

urlpatterns = [
    path("search/", views.StudentSearch.as_view(), name="student-search"),
    path("students/", views.StudentView.as_view(), name="student-list-create"),
    path("student/<int:pk>/", views.StudentDetailView.as_view(), name="student-detail"),
    path("student-count/", views.StudentCountView.as_view(), name="student-count"),
]

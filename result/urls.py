from django.urls import path
from .views import (
    AllResultView,
    UploadResultView,
    UpdateResultView,
    StudentResultHistoryView,
    GetStudentResult,
)

urlpatterns = [
    path('', AllResultView.as_view(), name='all'),  
    path('upload/', UploadResultView.as_view(), name='upload-result'),  
    path('<int:pk>/', UpdateResultView.as_view(), name='result-detail'),  
    path('student/<str:student_id>/', StudentResultHistoryView.as_view(), name='student-result-history'),  
    path('<str:registration_id>/', GetStudentResult.as_view(), name='student-recent-result'),
]

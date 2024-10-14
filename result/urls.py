from django.urls import path
from .views import AllResultView, UploadResultView, ResultDetailView, StudentResultHistoryView, StudentRecentResult

urlpatterns = [
    path('', AllResultView.as_view(), name='all'),  
    path('upload/', UploadResultView.as_view(), name='upload-result'),  
    path('<int:pk>/', ResultDetailView.as_view(), name='result-detail'),  
    path('student/<str:student_id>/', StudentResultHistoryView.as_view(), name='student-result-history'),  
    path('student/recent/', StudentRecentResult.as_view(), name='student-recent-result'),  
]

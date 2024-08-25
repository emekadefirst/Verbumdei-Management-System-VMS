from django.urls import path
from .views import *

urlpatterns = [
    path('classes/', ClassListCreateAPIView.as_view(), name='class-list-create'),
    path('classes/<int:pk>/', ClassRetrieveUpdateDestroyAPIView.as_view(), name='class-retrieve-update-destroy'),
    path('subjects/', SubjectListCreateAPIView.as_view(), name='subject-list-create'),
    path('subjects/<int:pk>/', SubjectRetrieveUpdateDestroyAPIView.as_view(), name='subject-retrieve-update-destroy'),
    path('subject-materials/', SubjectMaterialListCreateAPIView.as_view(), name='subject-material-list-create'),
    path('subject-materials/<int:pk>/', SubjectMaterialRetrieveUpdateDestroyAPIView.as_view(), name='subject-material-retrieve-update-destroy'),
]

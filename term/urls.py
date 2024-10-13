from django.urls import path
from .views import TermView, TermDetailView

urlpatterns = [
    path('all/', TermView.as_view(), name='term-list'),   
    path('detail/<int:pk>/', TermDetailView.as_view(), name='term-detail'),  
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.AnnouncementView.as_view(), name="create-announcement"),
    path("<int:pk>/", views.AnnouncementDetailView.as_view(), name="announcement-detail"),
]

from django.urls import path
from .views import ParentCountView, ParentDetailView, ParentView, ParentDashboard

urlpatterns = [
    path("", ParentView.as_view(), name="parent"),
    path("<int:pk>/", ParentDetailView.as_view(), name="parent_detail"),
    path("parent-count/", ParentCountView.as_view(), name="parent_count"),
    path("dashboard/<str:code>", ParentDashboard.as_view(), name="parent_count"),
]

from django.urls import path
from . import views


urlpatterns = [
    path(
        "attendance/create/<str:staff_id>/",
        views.CreateAttendanceView.as_view(),
        name="create-attendance",
    ),
    path("attendance/all/", views.AllAttendanceView.as_view(), name="all-attendance"),
    path(
        "attendance/class/<str:staff_id>/",
        views.AttendanceByClassView.as_view(),
        name="attendance-by-class",
    ),
    path(
        "attendance/student/<str:student_id>/",
        views.AttendanceByStudent.as_view(),
        name="attendance-by-student",
    ),
    path(
        "attendance/update/<str:staff_id>/",
        views.UpdateAttendanceView.as_view(),
        name="update-attendance",
    ),
]

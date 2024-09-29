from .models import Attendance
from django.contrib import admin


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "grade",
        "date",
        "present",
        "date",
        "count",
        "created_at",
    ]
    list_filter = ("grade", "date", "present", "created_at")
    search_fields = ("student__name", "grade__name", "created_at")
    date_hierarchy = "date"

    def get_readonly_fields(self, request, obj=None):
        if obj: 
            return ("student", "grade", "date")
        return ()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

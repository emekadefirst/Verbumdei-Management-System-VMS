from django.contrib import admin
from .models.attendance import AttendanceReport
from .models.term import Term


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "term",
        "class_assigned",
        "teacher",
        "response",
        "attendance_count",
        "date",
        "total_attendance_count",
    )

    readonly_fields = ("class_assigned", "teacher", "date", "total_attendance_count")

    def class_assigned(self, obj):
        return obj.class_assigned

    class_assigned.short_description = "Class Assigned"

    def teacher(self, obj):
        return obj.teacher

    teacher.short_description = "Teacher Assigned"


@admin.register(Term)
class TermtAdmin(admin.ModelAdmin):
    list_display = ["term", "session"]
    search_fields = ["term", "session"]
    list_filter = ["term", "session"]

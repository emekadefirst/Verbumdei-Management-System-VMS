from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Student, Attendance
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, ExportForm

@admin.register(Student)
class StudentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('registration_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'class_assigned', 'registration_date')
    search_fields = ('first_name', 'last_name', 'registration_id')
    list_filter = ('gender', 'class_assigned', 'registration_date')
    ordering = ('-registration_date',)
    readonly_fields = ('registration_id', 'registration_date')
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "grade", "date", "present")
    list_filter = ("grade", "date", "present")
    search_fields = ("student__name", "grade__name")
    date_hierarchy = "date"

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return ("student", "grade", "date")
        return ()

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

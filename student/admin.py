from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Student
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, ExportForm

@admin.register(Student)
class StudentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('registration_id', 'first_name', 'last_name', 'date_of_birth', 'gender', 'registration_date')
    search_fields = ('first_name', 'last_name', 'registration_id')
    list_filter = ('gender', 'registration_date')
    ordering = ('-registration_date',)
    readonly_fields = ('registration_id', 'registration_date')
    import_form_class = ImportForm
    export_form_class = ExportForm



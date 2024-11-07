from django.contrib import admin
from .models import Annoucement
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, ExportForm

@admin.register(Annoucement)
class AnnoucementAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['id', 'title', 'content', 'created_at']
    search_fields = ["id", "title", "content", "created_at"]
    list_filter = ["title", "content", "created_at"]
    ordering = ["-created_at"]
    readonly_fields = ["id", "created_at"]
    import_form_class = ImportForm
    export_form_class = ExportForm

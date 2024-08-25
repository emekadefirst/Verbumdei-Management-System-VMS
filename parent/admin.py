from django.contrib import admin
from .models import Parent
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, ExportForm, SelectableFieldsExportForm


@admin.register(Parent)
class ParentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['parent_name', 'phone_number_1', 'email', 'home_address']
    search_fields = ['parent_name', 'email', 'phone_number_1', 'phone_number_2']
    list_filter = ['home_address',]
    ordering = ['parent_name',]
    import_form_class = ImportForm
    export_form_class = ExportForm
   



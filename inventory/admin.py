from django.contrib import admin
from .models import InventoryType, Inventory
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm





@admin.register(InventoryType)
class InventoryTypeAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

@admin.register(Inventory)
class InventoryAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'type', 'quantity', 'time_of_purchase')
    list_filter = ('type', 'time_of_purchase')
    search_fields = ('name', 'type__name')
    ordering = ('-time_of_purchase',)
    readonly_fields = ('time_of_purchase',)
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

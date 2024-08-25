from .models import Class, Subject, SubjectMaterial
from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm

class ClassAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'teacher', 'created_at')
    search_fields = ('name', 'teacher__first_name', 'teacher__last_name')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm  

class SubjectAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'grade', 'teacher', 'created_at')
    search_fields = ('name', 'grade__name', 'teacher__first_name', 'teacher__last_name')
    list_filter = ('grade', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)    
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm  

class SubjectMaterialAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('subject', 'material', 'created_at')
    search_fields = ('subject__name', 'material')
    list_filter = ('subject', 'created_at')
    ordering = ['-created_at']
    readonly_fields = ['created_at']
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm  


admin.site.register(SubjectMaterial, SubjectMaterialAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Class, ClassAdmin)

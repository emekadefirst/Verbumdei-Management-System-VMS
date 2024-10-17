from .models import Class, Subject, SubjectMaterial
from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm

class ClassAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("name", "teacher", "student_count", "created_at")
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

from django.contrib import admin
from .models import SubjectMaterial


class SubjectMaterialAdmin(admin.ModelAdmin):
    list_display = ("subject", "upload", "material_url", "created_at")
    search_fields = ("subject__name",)

admin.site.register(SubjectMaterial, SubjectMaterialAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Class, ClassAdmin)

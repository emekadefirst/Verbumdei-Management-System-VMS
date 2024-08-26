from django.contrib import admin
from .models import PaymentType, Payment
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm


@admin.register(PaymentType)
class PaymentTypeAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["name", "cost"]
    search_fields = [
        "name",
    ]
    ordering = ["name"]
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm


@admin.register(Payment)
class PaymentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["payment_type", "student", "method", "status", "created_at"]
    search_fields = [
        "payment_type__name",
        "student__first_name",
        "student__last_name",
        "status",
    ]
    list_filter = ["method", "status", "created_at"]
    ordering = ["-created_at"]
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

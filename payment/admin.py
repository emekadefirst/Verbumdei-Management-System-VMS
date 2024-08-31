from django.contrib import admin
from .models import PaymentType, Payment
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm


@admin.register(PaymentType)
class PaymentTypeAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["name", "amount"]
    search_fields = [
        "name",
    ]
    ordering = ["name"]
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm


@admin.register(Payment)
class PaymentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["payment_type", "student", "method", "status", "reference", "created_at"]
    search_fields = [
        "payment_type__name",
        "student__first_name",
        "student__last_name",
        "status",
        "reference",
    ]
    list_filter = ["method", "status", "created_at"]
    ordering = ["-created_at"]
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm


# vb20827pa15
# VD20240827155323
# First Term School Fee
# Cash

{"parent": "vb20827pa15", "payment_type": "First Term School Fee", "student": "VD20240827155323", "method": "Online"}

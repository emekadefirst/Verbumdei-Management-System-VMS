from django.contrib import admin
from .models import PaymentType, Payment, PhysicalPayment
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm


@admin.register(PaymentType)
class PaymentTypeAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["payment_name", "amount"]
    search_fields = [
        "payment_name",
    ]
    ordering = ["payment_name"]
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm


@admin.register(Payment)
class PaymentAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ["payment_type", "student", "method", "status", "reference", "created_at"]
    search_fields = [
        "payment_type__payment_name",
        "student__first_name",
        "student__last_name",
        "status",
        "reference",
    ]
    list_filter = ["method", "status", "created_at"]
    ordering = ["-created_at"]
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm


class PhysicalPaymentAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "student",
        "term",
        "payment_name",
        "amount_paid",
        "balance",
        "status",
        "payment_id",
        "transaction_id",
        "time",
        "method",
    ]
    list_filter = ["status", "method", "term", "student"]
    search_fields = ["student__registration_id", "payment_id", "transaction_id"]
    ordering = ["-time"]
    readonly_fields = [
        "payment_id",
        "balance",
        "time",
        "id"
    ] 
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm 


admin.site.register(PhysicalPayment, PhysicalPaymentAdmin)

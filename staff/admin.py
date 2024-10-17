from django.contrib import admin
from .models import Staff, AccountInfo, Payroll
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm


@admin.register(Staff)
class StaffAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('staff_id', 'first_name', 'last_name', 'email', 'staff_type', 'employment_type', 'status')
    search_fields = ('staff_id', 'first_name', 'last_name', 'email', 'phone_number_1', 'nin')
    list_filter = ('staff_type', 'employment_type', 'status', 'gender', 'created_at', 'position', 'religion')
    ordering = ('-created_at',)
    readonly_fields = ('staff_id', 'created_at')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('bank_account')
        return queryset

@admin.register(AccountInfo)
class AccountInfoAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('staff', 'bank_name', 'account_number', 'account_name', 'sort_code')
    search_fields = ('staff__staff_id', 'staff__first_name', 'staff__last_name', 'bank_name', 'account_number')
    list_filter = ('bank_name',)
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm


@admin.register(Payroll)
class PayrollAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ("staff", "pay_period", "net_pay", "payment_status", "payment_date")
    search_fields = (
        "staff__staff_id",
        "staff__first_name",
        "staff__last_name",
        "transaction_reference",
    )
    list_filter = ("payment_status", "pay_period", "created_at", "updated_at")
    ordering = ("-pay_period", "staff__last_name")
    readonly_fields = (
        "transaction_reference",
        "created_at",
        "updated_at",
        "net_pay",
    )  # Make net_pay readonly
    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

    # def save_model(self, request, obj, form, change):
    #     if not obj.transaction_reference:
    #         obj.generate_transaction_reference()
    #     super().save_model(request, obj, form, change)

    # def get_queryset(self, request):
    #     queryset = super().get_queryset(request)
    #     queryset = queryset.select_related('staff', 'account_info')
    #     return queryset

from django.contrib import admin
from .models import Voucher
from inventory.models import InventoryType


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "type",
        "quantity",
        "unit_cost",
        "status",
        "code",
        "created_at",
    ]
    list_filter = ["status", "type", "created_at"]
    search_fields = ["name", "code", "type__name", "status"]
    ordering = ["-created_at"]
    readonly_fields = ["created_at"]

    fieldsets = [
        (
            "Voucher Information",
            {"fields": ["type", "name", "quantity", "unit_cost", "status"]},
        ),
        ("Timestamps", {"fields": ["created_at"]}),
    ]

    actions = ["approve_vouchers"]

from django.contrib import admin
from .models import Bus, Commute


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = [
        "plate_number",
        "manufacturer",
        "model",
        "year",
        "color",
        "sit_capacity",
        "driver",
        "created_at",
    ]
    search_fields = ["plate_number", "driver__staff_id"]
    list_filter = ["year", "sit_capacity", "color"]
    ordering = ["-created_at"]
    fields = [
        "plate_number",
        "manufacturer",
        "model",
        "year",
        "color",
        "sit_capacity",
        "driver",
    ]


@admin.register(Commute)
class CommuteAdmin(admin.ModelAdmin):
    list_display = ["uuid", "bus", "is_full"]
    search_fields = ["bus__plate_number", "uuid"]
    readonly_fields = ["uuid"]
    list_filter = ["bus"]
    ordering = ["-uuid"]
    filter_horizontal = ["students"]  
    fields = ["uuid", "bus", "students"]

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
    list_display = ["uuid", "bus", "get_student_count", "is_full"]
    search_fields = ["bus__plate_number", "uuid"]
    list_filter = ["bus"]
    ordering = ["-uuid"]
    filter_horizontal = ["student"]  
    fields = ["uuid", "bus", "student"]

    def get_student_count(self, obj):
        return obj.student.count()

    get_student_count.short_description = "Number of Students"

    def is_full(self, obj):
        return obj.is_full

    is_full.boolean = True
    is_full.short_description = "Is Full"

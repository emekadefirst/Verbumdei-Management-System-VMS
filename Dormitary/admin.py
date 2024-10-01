from django.contrib import admin
from .models import Hostel, Dorm


@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ["id", "type","warden",]
    list_filter = ["type", "warden",]
    search_fields = ["type",]
    ordering = ["type",]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("warden")


@admin.register(Dorm)
class DormAdmin(admin.ModelAdmin):
    list_display = ["id", "dorm_code","hostel", "max_occupants","current_occupants"]
    list_filter = ["hostel"]
    search_fields = ["dorm_code",]
    ordering = ["dorm_code",]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("occupants")

    def current_occupants(self, obj):
        return obj.current_occupants

    current_occupants.short_description = ("Current Occupants")

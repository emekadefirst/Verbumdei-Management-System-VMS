from django.contrib import admin
from .models import Hostel, Room



@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ["type", "warden"]  
    search_fields = [
        "type",
        "warden__first_name",
        "warden__last_name",
    ]  
    list_filter = ["type"]  

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "room_id",
        "hostel",
        "max_occupants",
        "current_occupants",
    ]  
    search_fields = ["room_id", "hostel__type"]  
    list_filter = ["hostel__type"]  
    filter_horizontal = ["occupants"]  
    readonly_fields = ["current_occupants"]  





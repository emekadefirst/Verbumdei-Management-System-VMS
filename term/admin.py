from django.contrib import admin
from .models.term import Term


@admin.register(Term)
class TermtAdmin(admin.ModelAdmin):
    list_display = ["term", "session", "name"]
    search_fields = ["term", "session", "name"]
    list_filter = ["term", "session", "name"]

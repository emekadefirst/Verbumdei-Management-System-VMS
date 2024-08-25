from django.contrib import admin
from .models import Event, Exam, Mid_Exam

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'created_at')
    search_fields = ('name', 'date')
    list_filter = ('date', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'created_at')
    search_fields = ('name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(Mid_Exam)
class MidExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'created_at')
    search_fields = ('name', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

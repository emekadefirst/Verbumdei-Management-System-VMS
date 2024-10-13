from django.contrib import admin
from .models import Result


class ResultAdmin(admin.ModelAdmin):
    list_display = [
        "student",
        "subject",
        "grade",
        "term",
        "teacher",
        "total_marks",
        "remark",
        "created_at",
    ]
    list_filter = ["subject", "grade", "term", "teacher", "created_at"]
    search_fields = [
        "student__first_name",
        "student__last_name",
        "subject__name",
        "teacher__first_name",
        "teacher__last_name",
    ]
    ordering = ["-created_at"]
    readonly_fields = [
        "total_marks",
        "remark",
        "created_at",
    ] 
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "student",
                    "subject",
                    "grade",
                    "term",
                    "teacher",
                    "continous_assessment",
                    "examination",
                ]
            },
        ),
        (
            "Results",
            {
                "fields": ["total_marks", "remark", "created_at"],
                "classes": ["collapse"],  
            },
        ),
    ]

admin.site.register(Result, ResultAdmin)

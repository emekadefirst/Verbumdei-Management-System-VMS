from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TeacherAdmin


class TeacherAdminAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "staff_id",
        "created_at",
        "is_staff",
    )

    list_filter = ("is_staff", "is_superuser", "is_active", "staff_id")

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "teacher_id",
        "staff__staff_id",
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "teacher_id", "staff_id")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    ordering = ("username",)
    def staff(self, obj):
        return obj.staff.staff_id if obj.staff else None


admin.site.register(TeacherAdmin, TeacherAdminAdmin)

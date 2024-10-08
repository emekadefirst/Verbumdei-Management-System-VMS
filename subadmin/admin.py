from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SubAdmin



class SubAdminAdmin(UserAdmin):
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
        "admin_id",
        "staff__staff_id",
    )

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "admin_id", "staff_id")},
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
                    "staff",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    ordering = ("username",)

    # Displays the field for staff association in the admin form
    def staff(self, obj):
        return obj.staff.staff_id if obj.staff else None

admin.site.register(SubAdmin, SubAdminAdmin)

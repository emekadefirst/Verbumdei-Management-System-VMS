from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import SubAdmin
from staff.models import Staff


# Custom admin interface for SubAdmin
class SubAdminAdmin(UserAdmin):
    # Fields to be displayed in the list view
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "admin_id",
        "staff",
        "created_at",
        "is_staff",
    )

    # Fields to filter the list view
    list_filter = ("is_staff", "is_superuser", "is_active", "staff")

    # Fields that can be searched
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "admin_id",
        "staff__staff_id",
    )

    # Fields that will be editable in the form view
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "email", "admin_id", "staff")},
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

    # Fields that will be displayed when creating a new SubAdmin
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

    # Defines the default ordering for the list view
    ordering = ("username",)

    # Displays the field for staff association in the admin form
    def staff(self, obj):
        return obj.staff.staff_id if obj.staff else None


# Register the SubAdmin model with the custom admin interface
admin.site.register(SubAdmin, SubAdminAdmin)

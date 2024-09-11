from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from staff.models import Staff


def admin_id():
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    return f"AD{date_str}{time_str}"


class SubAdmin(AbstractUser):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, null=True, blank=True)
    admin_id = models.CharField(
        max_length=25, default=admin_id, unique=True, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Add related_name to avoid clashes with auth.User model
    groups = models.ManyToManyField(
        "auth.Group", related_name="subadmin_groups", blank=True  # Custom related_name
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="subadmin_user_permissions",  # Custom related_name
        blank=True,
    )

    def __str__(self):
        return f"{self.username} - {self.admin_id}"

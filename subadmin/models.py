from django.contrib.auth.models import AbstractUser
from django.db import models


class SubAdmin(AbstractUser):
    staff_id = models.CharField(max_length=25, default=None, null=True, blank=True)
    admin_id = models.CharField(
        max_length=25, default=None, null=True, blank=True, unique=True
    )  
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        "auth.Group", related_name="subadmin_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="subadmin_user_permissions", blank=True
    )

    def save(self, *args, **kwargs):
        if not self.admin_id:
            self.admin_id = self.staff_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.admin_id}"

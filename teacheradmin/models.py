from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class TeacherAdmin(AbstractUser):
    staff_id = models.CharField(max_length=25, default=None, null=True, blank=True, unique=True)
    teacher_id = models.CharField(max_length=25, default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        "auth.Group", related_name="teacheradmin_groups_staff", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="teacheradmin_user_permissions_staff",
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.staff_id.startswith("t"):
            raise ValidationError("Invalid staff ID. Must start with 't'.")

        if not self.teacher_id:
            self.teacher_id = self.staff_id

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.staff_id}"

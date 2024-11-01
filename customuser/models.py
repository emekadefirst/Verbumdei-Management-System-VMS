from django.db import models
from staff.models import Staff
from parent.models import Parent
from datetime import datetime
from django.contrib.auth.models import AbstractUser


def userId(firstname):
    now = datetime.now()
    return f"{firstname}{now.strftime('%M%S')}"


class CustomUser(AbstractUser):
    class ROLE(models.TextChoices):
        HEAD_TEACHER = "HEAD TEACHER", "Head Teacher"
        TEACHER = "TEACHER", "Teacher"
        PARENT = "PARENT", "Parent"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"

    role = models.CharField(max_length=20, choices=ROLE.choices, default=ROLE.ADMIN)
    person_id = models.CharField(max_length=30, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("view_student_reports", "Can view student reports"),
            ("manage_student", "Can manage students"),
            ("manage_staff", "Can manage staff"),
            ("manage_event", "Can manage events"),
            ("manage_inventories", "Can manage inventories"),
        ]

    def save(self, *args, **kwargs):
        if self.person_id:
            try:
                staff_member = Staff.objects.get(staff_id=self.person_id)
                self.username = userId(staff_member.first_name)
            except Staff.DoesNotExist:
                try:
                    parent = Parent.objects.get(code=self.person_id)
                    self.username = userId(parent.parent_name)
                except Parent.DoesNotExist:
                    raise ValueError(
                        "Invalid `person_id`: no matching `Staff` or `Parent` found"
                    )
        super().save(*args, **kwargs)

        def __str__(self):
            result = self.person_id 
            if result is None:
                print("Warning: CustomUser __str__ method returned None")
            return result or "Unnamed User"


# adminv2.

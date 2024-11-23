from django.db import models
from staff.models import Staff
from parent.models import Parent
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class ROLE(models.TextChoices):
        HEAD_TEACHER = "HEAD TEACHER", "Head Teacher"
        TEACHER = "TEACHER", "Teacher"
        PARENT = "PARENT", "Parent"
        ACCOUNTANT = "ACCOUNTANT", "Accountant"
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Manager"
        SECRETARY = "SECRETARY", "Secretary"

    role = models.CharField(max_length=20, choices=ROLE.choices, default=ROLE.ADMIN)
    person_id = models.CharField(max_length=30,  unique=True)
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
            except Staff.DoesNotExist:
                try:
                    parent = Parent.objects.get(code=self.person_id)
                except Parent.DoesNotExist:
                    raise ValueError("Invalid `person_id`: no matching `Staff` or `Parent` found")
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return self.person_id


# adminv2.

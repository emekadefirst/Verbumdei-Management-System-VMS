from django.db import models
from datetime import datetime
from staff.models import Staff
from student.models import Student
from django.core.exceptions import ValidationError


def unique_room_id():
    now = datetime.now()
    time_str = now.strftime("%M%S")
    return f"ROOM{time_str}"


class Hostel(models.Model):
    class TYPE(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, choices=TYPE.choices, unique=True)
    warden = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        related_name="hostels",
        limit_choices_to={"staff_type": "NON_TEACHING"},
    )

    def __str__(self):
        return self.type


class Dorm(models.Model):
    id = models.AutoField(primary_key=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="rooms")
    dorm_code = models.CharField(max_length=10, unique=True, default=unique_room_id)
    max_occupants = models.PositiveIntegerField()
    occupants = models.ManyToManyField(Student, blank=True)

    @property
    def is_full(self):
        if self.occupants.count() == self.max_occupants:
            return True
        return False

    @property
    def current_occupants(self):
        return self.occupants.count()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.dorm_code

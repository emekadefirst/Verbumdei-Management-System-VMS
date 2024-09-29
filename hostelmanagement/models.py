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

    type = models.CharField(max_length=20, choices=TYPE.choices)
    warden = models.ForeignKey(
        Staff,
        on_delete=models.SET_NULL,
        null=True,
        related_name="hostels",
        limit_choices_to={"staff_type": "NON_TEACHING"},
    )

    def __str__(self):
        return f"{self.type} Hostel (Warden: {self.warden.first_name} {self.warden.last_name})"


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="rooms")
    room_id = models.CharField(max_length=10, unique=True, default=unique_room_id)
    max_occupants = models.PositiveIntegerField()
    occupants = models.ManyToManyField(
        Student, limit_choices_to={"type": "BOARDER"}, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["hostel", "room_id"], name="unique_room_per_hostel"
            )
        ]

    @property
    def current_occupants(self):
        return self.occupants.count()

    def clean(self):
        """Ensure the gender of the student matches the hostel type and room is not overfilled."""
        # Save the instance first before doing any many-to-many operations
        if self.pk is None:
            super().save()

        if self.current_occupants > self.max_occupants:
            raise ValidationError(f"Room {self.room_id} is already full.")

        for student in self.occupants.all():
            if student.gender != self.hostel.type:
                raise ValidationError(
                    f"Cannot assign {student.first_name} to {self.hostel.type} hostel."
                )

    def __str__(self):
        return f"Room {self.room_id} ({self.hostel.type} Hostel)"

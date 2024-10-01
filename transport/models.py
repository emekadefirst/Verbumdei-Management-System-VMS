from django.db import models
from staff.models import Staff
from student.models import Student
from django.core.exceptions import ValidationError
import uuid


class Bus(models.Model):
    id = models.AutoField(primary_key=True)
    plate_number = models.CharField(max_length=15, unique=True)
    manufacturer = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)
    year = models.CharField(max_length=5, null=True)
    color = models.CharField(max_length=55, blank=True, null=True)
    sit_capacity = models.IntegerField()
    driver = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name="bus",
        limit_choices_to={"staff_type": "NON_TEACHING"},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bus {self.plate_number} - Driver: {self.driver}"


class Commute(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    bus = models.ForeignKey(
        Bus,
        on_delete=models.CASCADE,
    )
    students = models.ManyToManyField(Student, related_name="commutes")

    @property
    def is_full(self):
        return self.bus.sit_capacity == self.students.count()

    def add_student(self, student):
        if not self.is_full:
            self.students.add(student)
        else:
            raise ValidationError(f"{self.bus.plate_number} is full.")

    def __str__(self):
        return f"Commute {self.uuid} - Bus: {self.bus.plate_number}"

    class Meta:
        unique_together = ("uuid", "bus")

from django.db import models
from grade.models import Class
from student.models import Student


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="attendances"
    )
    grade = models.ForeignKey(
        Class, on_delete=models.CASCADE, related_name="attendances"
    )
    date = models.DateField()
    present = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["-created_at"]
    
    @property
    def count(self):
        return 1 if self.present else 0


    def __str__(self):
        return f"Attendance for {self.student.registration_id} in {self.grade.name} on {self.date}"

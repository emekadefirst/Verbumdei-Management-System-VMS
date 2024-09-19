from django.db import models
from student.models import Student
from .term import Term


class AttendanceReport(models.Model):
    term = models.ForeignKey(
        Term, on_delete=models.CASCADE, related_name="attendance_reports", default=None
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="attendance_reports"
    )
    response = models.BooleanField(default=False)
    attendance_count = models.PositiveBigIntegerField(default=1) 
    date = models.DateField(auto_now_add=True)

    @property
    def class_assigned(self):
        return self.student.class_assigned.name

    @property
    def teacher(self):
        return self.student.class_assigned.teacher.staff_id

    def increment_attendance(self):
        if self.response:  
            self.attendance_count += 1
            self.save()

    @property
    def total_attendance_count(self):
        return sum(
            report.attendance_count for report in self.student.attendance_reports.all()
        )

    def __str__(self):
        return f"{self.student.registration_id} - {self.class_assigned} on {self.date}"

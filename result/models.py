from django.db import models
from student.models import Student
from grade.models import Subject, Class
from staff.models import Staff
from term.models.term import Term

class Result(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    grade = models.ForeignKey(Class, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, limit_choices_to={"staff_type": "NON_TEACHING"})
    continous_assessment = models.PositiveBigIntegerField(null=True, blank=True)
    examination = models.PositiveBigIntegerField(null=True, blank=True)
    total_marks = models.PositiveBigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    remark = models.CharField(max_length=15)
    
    def save(self, *args, **kwargs):
        
        if self.continous_assessment is not None and self.examination is not None:
            self.total_marks = self.continous_assessment + self.examination
            
            if self.total_marks in range(35, 50):
                self.remark = "PASSED"
            elif self.total_marks in range(50, 66):
                self.remark = "AVERAGE"
            elif self.total_marks in range(66, 70):
                self.remark = "GOOD"
            elif self.total_marks in range(70, 76):
                self.remark = "VERY GOOD"
            elif self.total_marks in range(76, 86):
                self.remark = "EXCELLENT"
            elif self.total_marks > 86:
                self.remark = "DISTINCTION"
            elif self.total_marks < 35:
                self.remark = "FAILED"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.student.registration_id
    
    


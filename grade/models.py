from django.db import models
from django.core.exceptions import ValidationError
from staff.models import Staff

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12, unique=True)
    teacher = models.OneToOneField(Staff, on_delete=models.CASCADE, limit_choices_to={'staff_type': 'TEACHING'})
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if self.teacher.staff_type != 'TEACHING':
            raise ValidationError(f'Teacher {self.teacher} is not a teaching staff member.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Subject(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    grade = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, limit_choices_to={'staff_type': 'TEACHING'})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SubjectMaterial(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='study_materials')
    material = models.FileField(upload_to='study_materials/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Material for {self.subject.name} - {self.material.name}"

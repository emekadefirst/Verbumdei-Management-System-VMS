from django.db import models
from django.core.exceptions import ValidationError
from staff.models import Staff
from server.cloud import cloud_doc, cloud
from io import BytesIO
from django.utils.text import slugify
from student.models import Student
from django.contrib.auth.models import AbstractUser


class Class(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=12, unique=True)
    teacher = models.OneToOneField(Staff, on_delete=models.CASCADE, limit_choices_to={'staff_type': 'TEACHING'})
    students = models.ManyToManyField(Student)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def student_count(self):
        return self.students.count()
    
    
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
    upload = models.FileField(upload_to="Subject_material/", blank=True, null=True)
    material_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.upload:
            if not self.material_url:
                upload_file = self.upload.read()
                sanitized_name = slugify(self.upload.name, allow_unicode=False)
                file_url = cloud_doc(BytesIO(upload_file), sanitized_name)
                if file_url:
                    self.material_url = file_url
                self.upload.delete(save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Material for {self.subject.name} - {self.material_url}"

    def __str__(self):
        return f"Material for {self.subject.name} - {self.material_url}"

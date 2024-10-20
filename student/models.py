from django.db import models
from datetime import datetime
from parent.models import Parent
from server.cloud import cloud
from io import BytesIO
from django.utils.text import slugify


def student_registration_id():
    now = datetime.now()
    date_str = now.strftime('%Y%m%d')
    time_str = now.strftime('%H%M%S')
    return f'VD{date_str}{time_str}'

class Student(models.Model):
    class GENDER(models.TextChoices):
        MALE = "MALE", "male"
        FEMALE = "FEMALE", "female" 
    class TYPE(models.TextChoices):
        DAY = "DAY", "day"
        FEMALE = "BOARDER", "boarder" 
    type = models.CharField(max_length=20, choices=TYPE.choices) 
    id = models.AutoField(primary_key=True)
    registration_id = models.CharField(max_length=20, default=student_registration_id, unique=True)
    first_name = models.CharField(max_length=25)
    other_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=20, choices=GENDER.choices)
    home_address = models.CharField(max_length=100)
    state_of_origin = models.CharField(max_length=20)
    local_government_area = models.CharField(max_length=20)
    nationality = models.CharField(max_length=20)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    religion = models.CharField(max_length=20)
    upload = models.ImageField(upload_to="Student_profile/", null=True, blank=True)
    img_url = models.URLField(max_length=500, blank=True)
    registration_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.upload and not self.img_url:
            sanitized_name = slugify(self.upload.name, allow_unicode=False)
            image_data = BytesIO(self.upload.read())
            self.img_url = cloud(image_data, sanitized_name)
            self.upload.delete(save=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-registration_date']

    def __str__(self):
        fullname = f"{self.first_name} {self.last_name} {self.other_name}"
        return fullname



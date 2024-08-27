from django.db import models
from datetime import datetime
from parent.models import Parent
from grade.models import Class

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
    profile_image = models.ImageField(upload_to="Student_profile/")
    class_assigned = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    registration_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-registration_date']
        
    def __str__(self):
        return self.registration_id
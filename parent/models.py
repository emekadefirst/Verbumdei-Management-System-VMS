from django.db import models
from datetime import datetime


def parent_id():
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    return f"vb{date_str}pa{time_str}"


class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50)
    phone_number_1 = models.CharField(max_length=14)
    phone_number_2 = models.CharField(max_length=14)
    parent_name = models.CharField(max_length=25)
    home_address = models.CharField(max_length=150)
    code = models.CharField(max_length=12, default=parent_id, unique=True)

    def __str__(self):
        return f"{self.code} - {self.email}"

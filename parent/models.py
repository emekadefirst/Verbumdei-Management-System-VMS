from django.db import models

class Parent(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=50)
    phone_number_1 = models.CharField(max_length=14)
    phone_number_2 = models.CharField(max_length=14)
    parent_name = models.CharField(max_length=25)
    home_address = models.CharField(max_length=150)
    
    def __str__(self):
        return f"{self.parent_name} - {self.phone_number_1} - {self.email}"

from django.db import models

class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        
class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='First Term Exam')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        
class Mid_Exam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, default='First Term Mid Exam')
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

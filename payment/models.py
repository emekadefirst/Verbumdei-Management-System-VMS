from django.db import models
from student.models import Student


class PaymentType(models.Model):
    name = models.CharField(max_length=150)
    cost = models.FloatField()

    def __str__(self):
        return self.name


class Payment(models.Model):
    class PAYMENT_METHOD(models.TextChoices):
        ONLINE = "ONLINE", "Online"
        CASH = "CASH", "Cash"
        POS = "POS", "Point of Sale"

    id = models.AutoField(primary_key=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD.choices)
    status = models.CharField(max_length=12)
    created_at = models.DateTimeField(auto_now_add=True)

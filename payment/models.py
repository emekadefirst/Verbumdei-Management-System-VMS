from django.db import models
from student.models import Student
from parent.models import Parent


class PaymentType(models.Model):
    name = models.CharField(max_length=150)
    amount = models.FloatField()

    def __str__(self):
        return self.name


class Payment(models.Model):
    class PAYMENT_METHOD(models.TextChoices):
        ONLINE = "ONLINE", "online"
        CASH = "CASH", "cash"
        POS = "POS", "point of Sale"
    id = models.AutoField(primary_key=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD.choices)
    status = models.CharField(max_length=12, default='processing')
    reference = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.payment_type} - {self.reference}"

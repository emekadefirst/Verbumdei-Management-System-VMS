from django.db import models
from student.models import Student
from parent.models import Parent
from datetime import datetime
from term.models.term import Term
from grade.models import Class

def generate_payment_id():
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    return f"{date_str}{time_str}"


class PaymentType(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=1000, null=True, blank=True, unique=True)
    payment_name = models.CharField(max_length=255)
    grade = models.ForeignKey(Class, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.term and self.grade:
            self.title = f"{self.payment_name} {self.grade.name} {self.term.name}"

        super().save(*args, **kwargs)
    def __str__(self):
        return self.title


class PhysicalPayment(models.Model):
    class STATUS(models.TextChoices):
        COMPLETED = "COMPLETED", "Completed"
        OUTSTANDING = "OUTSTANDING", "Outstanding"
        NOT_PAID = "NOT_PAID", "Not paid"
    class METHOD(models.TextChoices):
        POS = "POS", "POS"
        CASH = "CASH", "Cash"
        TRANSFER = "TRANSFER", "Transfer"
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    payment_name = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    amount_paid = models.FloatField(default=0.00)
    balance = models.FloatField(default=0.00)
    status = models.CharField(max_length=30, choices=STATUS.choices, default=STATUS.NOT_PAID)
    payment_id = models.CharField(max_length=30, unique=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)  
    time = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=30, choices=METHOD.choices, default=METHOD.CASH)

    @property
    def payment_cost(self):
        return self.payment_name.amount

    def save(self, *args, **kwargs):
        if not self.payment_id:
            self.payment_id = generate_payment_id()
        if self.method in [self.METHOD.POS, self.METHOD.TRANSFER]:
            if not self.transaction_id:
                raise ValueError("Transaction ID is required for POS and Transfer payments.")
        elif self.method == self.METHOD.CASH:
            self.transaction_id = None
        self.balance = self.payment_cost - self.amount_paid
        if self.balance > 0:
            self.status = self.STATUS.OUTSTANDING
        elif self.balance == 0:
            self.status = self.STATUS.COMPLETED
        else:
            self.balance = 0 
            self.status = self.STATUS.COMPLETED
        if self.amount_paid == 0.00:
            self.status = self.STATUS.NOT_PAID
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-time"]

    def __str__(self):
        return self.student.registration_id


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

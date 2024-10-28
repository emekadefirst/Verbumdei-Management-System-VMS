import uuid
import random
from django.db import models
from django.utils import timezone
from student.models import Student


def generate_sh_code():
    random_number = random.randint(100000, 999999)
    return f"SH{random_number}"

class BookCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name


class Shelf(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  
    code = models.CharField(max_length=10, null=True, default=generate_sh_code, unique=True)  
    location = models.CharField(max_length=100)  
    section = models.CharField(max_length=100)  
    description = models.TextField(null=True, blank=True)  

    def __str__(self):
        return f"Shelf {self.code} - {self.section} - {self.location}"


class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    isbn = models.CharField(max_length=100, unique=True)
    copies = models.PositiveIntegerField()
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
    shelf = models.ForeignKey(Shelf, on_delete=models.SET_NULL, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Loan(models.Model):
    class Action(models.TextChoices):
        BORROW = "BORROWED", "Borrowed"
        RETURN = "RETURNED", "Returned"

    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    action = models.CharField(
        max_length=10,
        choices=Action.choices,
        default=Action.BORROW
    )
    borrowed_at = models.DateTimeField(auto_now_add=True) 
    return_date = models.DateTimeField(null=True, blank=True) 
    actual_return_date = models.DateTimeField(null=True, blank=True) 

    def __str__(self):
        fullname = f"{self.student.first_name} {self.student.last_name} {self.student.other_name}"
        return f"{self.book.title} - {fullname} ({self.event})"

    def is_overdue(self):
        if self.actual_return_date is None and self.return_date and self.return_date < timezone.now():
            return True
        return False

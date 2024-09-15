from django.db import models
from datetime import datetime
from django.db.models import Sum
import uuid
from server.cloud import cloud
from io import BytesIO
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


def staff_registration_id(staff_type):
    now = datetime.now()
    date_str = now.strftime("%Y%m%d")
    time_str = now.strftime("%H%M%S")
    prefix = "t" if staff_type == "TEACHING" else "n"
    return f"{prefix}STF{date_str}{time_str}"


class Staff(models.Model):
    class EMPLOYMENT_TYPE(models.TextChoices):
        FULLTIME = "FULLTIME", "Fulltime"
        GRADUATE_ASSISTANT = "GRADUATE_ASSISTANT", "Graduate Assistant"
        PART_TIME = "PART_TIME", "Part-time"
        INTERN = "INTERN", "Intern"
        CORPER = "CORPER", "Corper"

    class STATUS(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"

    class GENDER(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"

    class STAFF_TYPE(models.TextChoices):
        TEACHING = "TEACHING", "Teaching"
        NON_TEACHING = "NON_TEACHING", "Non-teaching"

    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=20, choices=GENDER.choices)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    other_name = models.CharField(max_length=15, blank=True, null=True)
    phone_number_1 = models.CharField(max_length=15)
    phone_number_2 = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE.choices)
    home_address = models.CharField(max_length=55)
    local_government_area = models.CharField(max_length=100)
    state_of_origin = models.CharField(max_length=15)
    nin = models.CharField(max_length=11, unique=True)
    bvn = models.CharField(max_length=11, unique=True)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPE.choices)
    staff_id = models.CharField(max_length=25, unique=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS.choices)
    position = models.CharField(max_length=20)
    upload = models.ImageField(upload_to="Staff_profile/", blank=True, null=True)
    img_url = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.staff_id:
            self.staff_id = staff_registration_id(self.staff_type)
        if self.upload and not self.img_url:
            sanitized_name = slugify(self.upload.name, allow_unicode=False)
            image_data = BytesIO(self.upload.read())
            self.img_url = cloud(image_data, sanitized_name)
            self.upload.delete(save=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        fullname = f"{self.first_name} {self.last_name} {self.other_name}"
        return fullname.strip()


class AccountInfo(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='bank_account')
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    account_name = models.CharField(max_length=100)
    sort_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.staff.staff_id} - {self.bank_name} - {self.account_number}"


class Payroll(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PROCESSED = "PROCESSED", "Processed"
        PAID = "PAID", "Paid"

    id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(
        Staff, on_delete=models.SET_NULL, null=True, related_name="payrolls"
    )
    pay_period = models.DateField()
    account_info = models.ForeignKey(AccountInfo, on_delete=models.SET_NULL, null=True)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_pay = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )  
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    payment_date = models.DateField(null=True, blank=True)
    transaction_reference = models.CharField(
        max_length=50, unique=True, blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-pay_period", "staff__last_name"]
        unique_together = ["staff", "pay_period"]

    def __str__(self):
        return f"{self.staff} - {self.pay_period.strftime('%B %Y')}"

    def save(self, *args, **kwargs):
        self.calculate_net_pay()
        if not self.transaction_reference:
            self.generate_transaction_reference()
        super().save(*args, **kwargs)

    def calculate_net_pay(self):
        self.net_pay = self.basic_salary + self.allowances - self.deductions

    def generate_transaction_reference(self):
        self.transaction_reference = f"PAY-{self.staff.staff_id}{self.pay_period.strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"


class TeacherAdmin(AbstractUser):
    staff_id = models.CharField(max_length=25, default=None, null=True, blank=True)
    admin_id = models.CharField(
        max_length=25, default=None, null=True, blank=True
    ) 
    created_at = models.DateTimeField(auto_now_add=True)
    groups = models.ManyToManyField(
        "auth.Group", related_name="teacheradmin_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="teacheradmin_user_permissions", blank=True
    )

    def save(self, *args, **kwargs):
        if not self.admin_id:
            self.admin_id = self.staff_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - {self.admin_id}"

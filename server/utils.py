from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from staff.models import Staff
from student.models import Student
from payment.models import Payment
import json


def dashboard_callback(request, context=None):
    # Get the last 7 days of data
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)

    # Payment data for the last 7 days
    payments_last_7_days = (
        Payment.objects.filter(created_at__date__range=[start_date, end_date])
        .values("created_at__date")
        .annotate(amount=Sum("payment_type__amount"))
        .order_by("created_at__date")
    )

    payments_data = [
        {
            "date": payment["created_at__date"].strftime("%Y-%m-%d"),
            "amount": float(payment["amount"]),
        }
        for payment in payments_last_7_days
    ]

    # Student registration data for the last 7 days
    student_registrations = (
        Student.objects.filter(registration_date__date__range=[start_date, end_date])
        .values("registration_date__date")
        .annotate(count=Count("id"))
        .order_by("registration_date__date")
    )

    student_data = [
        {
            "date": reg["registration_date__date"].strftime("%Y-%m-%d"),
            "count": reg["count"],
        }
        for reg in student_registrations
    ]

    # Total statistics
    total_staff = Staff.objects.count()
    total_payments = (
        Payment.objects.aggregate(total=Sum("payment_type__amount"))["total"] or 0
    )

    # Get the total count of students
    total_students = Student.objects.count()

    # Prepare the new context data
    new_context = {
        "payments_last_7_days": json.dumps(payments_data),
        "student_registration_graph_data": json.dumps(student_data),
        "total_staff": total_staff,
        "total_payments": total_payments,
        "total_students": total_students,  # Add the total student count
    }

    # If a context was provided, update it with our new data
    if context is not None:
        context.update(new_context)
        return context
    else:
        return new_context

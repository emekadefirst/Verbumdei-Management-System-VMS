from django.db.models import Count, Sum
from django.db.models.functions import TruncDay
from django.utils import timezone
from datetime import timedelta
import json
from student.models import Student
from staff.models import Staff
from payment.models import Payment

def dashboard_callback(request, context):
    # Basic counts
    context.update({
        "total_staff": Staff.objects.count(),
        "total_student": Student.objects.count(),
        "total_payment": Payment.objects.aggregate(total_amount=Sum('amount'))['total_amount'] or 0,
    })

    # Prepare data for charts
    last_7_days = timezone.now() - timedelta(days=7)

    # Total payments in the last 7 days
    payments_last_7_days = Payment.objects.filter(created_at__gte=last_7_days)\
        .annotate(day=TruncDay('created_at'))\
        .values('day')\
        .annotate(total_amount=Sum('amount'))\
        .order_by('day')

    context['payments_last_7_days'] = json.dumps(
        [{'date': item['day'].strftime('%Y-%m-%d'), 'amount': item['total_amount']} for item in payments_last_7_days]
    )

    # Student Registration Analytics
    # Example: Count students created in the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    student_registration_stats = Student.objects.filter(created_at__gte=thirty_days_ago)\
        .annotate(day=TruncDay('created_at'))\
        .values('day')\
        .annotate(count=Count('id'))\
        .order_by('day')

    context['student_registration_graph_data'] = json.dumps(
        [{'date': item['day'].strftime('%Y-%m-%d'), 'count': item['count']} for item in student_registration_stats]
    )

    return context

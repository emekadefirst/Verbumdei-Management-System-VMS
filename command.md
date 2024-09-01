#Generate secret keys

#Run
"./manage.py shell" or "python manage.py shell"
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())

{
  "username": "test_user",
  "password": "test_password",
  "email": "test@example.com"
}

./manage.py makemigrations api --empty
Migrations for 'api':
  api\migrations\0001_initial.py


gunicorn --workers 3 --bind 0.0.0.0:8000 server.wsgi:application --env DJANGO_SETTINGS_MODULE=server.settings.production
gunicorn server.wsgi:application
gunicorn server.wsgi:application --workers 3 --bind 0.0.0.0:8000


{
    "parent": "vb20827pa15",
    "payment_type": "First Term School Fee",
    "student": "VD20240827155323",
    "method": "CASH"
}
https://verbumdei-management-system-vms.onrender.com/payment/make-payment/



{
  "event": "paymentrequest.success",
  "data": {
    "id": 1089700,
    "domain": "test",
    "amount": 10000000,
    "currency": "NGN",
    "due_date": null,
    "has_invoice": false,
    "invoice_number": null,
    "description": "Pay up now",
    "pdf_url": null,
    "line_items": [],
    "tax": [],
    "request_code": "PRQ_y0paeo93jh99mho",
    "status": "success",
    "paid": true,
    "paid_at": "2019-06-21T15:26:10.000Z",
    "metadata": null,
    "notifications": [
      {
        "sent_at": "2019-06-21T15:25:42.452Z",
        "channel": "email"
      }
    ],
    "offline_reference": "3365451089700",
    "customer": 7454223,
    "created_at": "2019-06-21T15:25:42.000Z"
  }
}
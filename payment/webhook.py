import requests
from .models import Payment
from .serializers import PaymentSerializers
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import json



@require_POST
def webhook(request):
    event = json.loads(request.body)
    return HttpResponse(status=200)

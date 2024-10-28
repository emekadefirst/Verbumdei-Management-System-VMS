from .models import CustomUser
from django.contrib.auth.backends import BaseBackend


class CustomBackend(BaseBackend):
    def authenticate(self, request, person_id=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(person_id=person_id)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None

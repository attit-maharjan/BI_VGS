from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from .models import Person

class PersonBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            person = Person.objects.get(email=username)
            if person.check_password(password):
                # Get or create a Django User for the Person
                user, _ = User.objects.get_or_create(
                    username=person.email,
                    defaults={
                        'email': person.email,
                        'first_name': person.first_name,
                        'last_name': person.last_name
                    }
                )
                return user
        except Person.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = CharField(_("Name of User"), blank=True, max_length=255)
    # disable first and last name attributes of a user, move them to Profile model later
    first_name = None
    last_name = None
    
    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})

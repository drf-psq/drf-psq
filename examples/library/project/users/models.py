from django.db import models
from django.contrib.auth.models import AbstractUser

from ..libraries.models import Library


class User(AbstractUser):

    registered_library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True)

from django.db import models

from ..libraries.models import Library


class Book(models.Model):

    name = models.CharField(max_length=50)
    library = models.ForeignKey(Library, on_delete=models.SET_NULL, null=True)

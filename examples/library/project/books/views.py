from rest_framework import viewsets
from rest_framework import mixins

from drf_psq import PsqMixin, Rule

from .models import Book
from .serializers import BookSerializer
from ..libraries.permissions import IsRegisteredInLibrary


class BookViewSet(PsqMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsRegisteredInLibrary]

    psq_rules = {
        'retrieve': [Rule(get_obj=lambda self, obj: obj.library)]
    }

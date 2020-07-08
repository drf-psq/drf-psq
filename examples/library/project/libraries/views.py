from rest_framework import viewsets
from rest_framework import mixins

from .models import Library
from .serializers import LibrarySerializer
from .permissions import IsRegisteredInLibrary


class LibraryViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsRegisteredInLibrary]

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import BookViewSet


router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]

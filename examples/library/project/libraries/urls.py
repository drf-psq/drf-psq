from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import LibraryViewSet


router = DefaultRouter()
router.register(r'libraries', LibraryViewSet, basename='library')

urlpatterns = [
    url(r'^', include(router.urls))
]

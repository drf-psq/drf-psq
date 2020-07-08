from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import UserViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]

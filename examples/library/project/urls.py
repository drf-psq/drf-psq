from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url


urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'^', include('project.users.urls')),
    url(r'^', include('project.libraries.urls')),
    url(r'^', include('project.books.urls')),
]

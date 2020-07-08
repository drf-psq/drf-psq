from django.contrib import admin
from .models import Library


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):

    list_display = ('name', )
    search_fields = ('name', )

from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = ('name', 'library')
    search_fields = ('name', 'library')

import random
import string

from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token

from ..users.models import User
from ..libraries.models import Library
from ..books.models import Book


class BookTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.lib1 = Library.objects.create(name='lib1')
        self.lib2 = Library.objects.create(name='lib2')

        self.book11 = Book.objects.create(name='book1-1', library=self.lib1)
        self.book12 = Book.objects.create(name='book1-2', library=self.lib1)
        self.book21 = Book.objects.create(name='book2-1', library=self.lib2)
        self.book22 = Book.objects.create(name='book2-2', library=self.lib2)

        self.user1 = User.objects.create_user(
            username='user1', password="".join(random.choices(string.ascii_letters, k=10)),
            registered_library=self.lib1
        )
        self.user2 = User.objects.create_user(
            username='user2', password="".join(random.choices(string.ascii_letters, k=10)),
            registered_library=self.lib2
        )

        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)

        self.header1 = {'HTTP_AUTHORIZATION': 'Token ' + self.token1.key}
        self.header2 = {'HTTP_AUTHORIZATION': 'Token ' + self.token2.key}


    def test_user_permitted(self):
        response = self.client.get(
            reverse('book-detail', kwargs=dict(pk=self.book11.pk)), **self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('book-detail', kwargs=dict(pk=self.book12.pk)), **self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_user_not_permitted(self):
        response = self.client.get(
            reverse('book-detail', kwargs=dict(pk=self.book21.pk)), **self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(
            reverse('book-detail', kwargs=dict(pk=self.book22.pk)), **self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

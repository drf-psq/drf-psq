import random
import string
import json

from django.test import TestCase, Client
from django.urls import reverse

from rest_framework import status
from rest_framework.authtoken.models import Token

from ..users.models import User
from ..libraries.models import Library
from ..books.models import Book


class UserTest(TestCase):

    def setUp(self):
        self.client = Client()

        self.lib1 = Library.objects.create(name='lib1')
        self.lib2 = Library.objects.create(name='lib2')

        self.book11 = Book.objects.create(name='book1-1', library=self.lib1)
        self.book12 = Book.objects.create(name='book1-2', library=self.lib1)
        self.book13 = Book.objects.create(name='book1-3', library=self.lib1)
        self.book21 = Book.objects.create(name='book2-1', library=self.lib2)
        self.book22 = Book.objects.create(name='book2-2', library=self.lib2)
        self.book23 = Book.objects.create(name='book2-3', library=self.lib2)

        self.user1 = User.objects.create_user(
            username='user1', password="".join(random.choices(string.ascii_letters, k=10)),registered_library=self.lib1
        )
        self.user2 = User.objects.create_user(
            username='user2', password="".join(random.choices(string.ascii_letters, k=10)), registered_library=self.lib2
        )

        self.admin1 = User.objects.create_user(
            username='admin1', password="".join(random.choices(string.ascii_letters, k=10)),
            registered_library=self.lib1, is_staff=True, is_active=False
        )
        self.admin2 = User.objects.create_user(
            username='admin2', password="".join(random.choices(string.ascii_letters, k=10)),
            registered_library=self.lib1, is_superuser=True, is_staff=True
        )

        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        self.token3 = Token.objects.create(user=self.admin1)
        self.token4 = Token.objects.create(user=self.admin2)

        self.header1 = {'HTTP_AUTHORIZATION': 'Token ' + self.token1.key}
        self.header2 = {'HTTP_AUTHORIZATION': 'Token ' + self.token2.key}
        self.header3 = {'HTTP_AUTHORIZATION': 'Token ' + self.token3.key}
        self.header4 = {'HTTP_AUTHORIZATION': 'Token ' + self.token4.key}

        self.payload = {
            'username': 'newuser',
            'password': '123123'
        }

        self.updated_payload = {
            'username': 'updated_user2',
            'password': '123123',
            'is_staff': True
        }


    def test_retrive_user(self):
        response = self.client.get(
            reverse('user-detail', kwargs=dict(pk='me')), **self.header1
        )
        self.assertEqual(response.data['registered_library'], self.lib1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(KeyError):
            response.data['is_active']

        response = self.client.get(
            reverse('user-detail', kwargs=dict(pk='me')), **self.header3
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(
            reverse('user-detail', kwargs=dict(pk='me')), **self.header4
        )
        self.assertTrue(response.data['is_active'])

        response = self.client.get(
            reverse('user-detail', kwargs=dict(pk=5)), **self.header4
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_list_user(self):
        response = self.client.get(
            reverse('user-list'), **self.header1
        )
        self.assertEqual(response.data[0]['registered_library'], self.lib1.id)
        self.assertEqual(response.data[1]['registered_library'], self.lib2.id)


    def test_create_user(self):
        response = self.client.post(
            reverse('user-list'), data=json.dumps(self.payload),
            content_type='application/json', **self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(
            reverse('user-list'), data=json.dumps(self.payload),
            content_type='application/json', **self.header4
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_update_user(self):
        response = self.client.put(
            reverse('user-detail', kwargs=dict(pk=self.user2.pk)),
            data = json.dumps(self.updated_payload),
            content_type = 'application/json',
            **self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.put(
            reverse('user-detail', kwargs=dict(pk=self.user2.pk)),
            data = json.dumps(self.updated_payload),
            content_type = 'application/json',
            **self.header4
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_staff'])


    def test_delete_user(self):
        response = self.client.delete(
            reverse('user-detail', kwargs=dict(pk=self.user2.pk)),
            content_type = 'application/json',
            **self.header1
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(
            reverse('user-detail', kwargs=dict(pk=self.user2.pk)),
            content_type = 'application/json',
            **self.header4
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(
            reverse('user-detail', kwargs=dict(pk=self.user2.pk)), **self.header4
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# Django
from django.urls import reverse

# Rest Framework
from rest_framework.test import APITestCase
from rest_framework import status


class TestViews(APITestCase):

    def setUp(self):
        self.register_url = reverse('signup')
        self.login_url = reverse('login')

        self.register_data = {
            "email": "testuser@mail.com",
            "password": "test123456",
        }

        self.login_data_email = {
            "email": "testuser@mail.com",
            "password": "",
        }

        self.login_data_username = {
            "username": "testuser",
            "password": "test123456",
        }

    def test_user_cannot_register_without_full_data(self):
        """A user will not be able to register without the complete fields which are:
         email, password and password confirmation"""
        response_register = self.client.post(self.register_url, self.register_data)
        self.assertEqual(response_register.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_login_with_void_or_incomplete_fields(self):
        """A user will not be able to log in if the fields or any field is blank"""
        response_login = self.client.post(self.login_url, self.login_data_email)
        self.assertEqual(response_login.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_login_with_username_instead_of_email(self):
        """A user will not be able to log in if he tries to log in
         with his username instead of his email"""
        response_login = self.client.post(self.login_url, self.login_data_username)
        self.assertEqual(response_login.status_code, status.HTTP_400_BAD_REQUEST)

# Django
from django.urls import reverse

# Rest Framework
from rest_framework.test import APITestCase


class TestViews(APITestCase):

    def setUp(self):
        self.register_url = reverse('signup')
        self.login_url = reverse('login')

        self.register_data = {
            "email": "testuser@mail.com",
            "password": "test123456",
        }

        self.login_data = {
            "email": "testuser@mail.com",
            "password": "",
        }

    def test_user_cannot_register_without_full_data(self):
        response_register = self.client.post(self.register_url, self.register_data)
        self.assertEqual(response_register.status_code, 400)

    def test_user_cannot_login_with_void_fields(self):
        response_login = self.client.post(self.login_url, self.login_data)
        self.assertNotEqual(response_login.status_code, 200)
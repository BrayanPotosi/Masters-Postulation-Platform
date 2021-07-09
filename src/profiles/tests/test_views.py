# Django
from django.urls import reverse

# Rest Framework
from rest_framework.test import APITestCase

# Mommy
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key


class TestViews(APITestCase):

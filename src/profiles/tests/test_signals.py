# Django
from django.test import TestCase

# Mommy
from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

# Models
from ..models import Profile


class TestSignal(TestCase):
    """Check if a user's profile is created when initializing an instance"""

    def setUp(self):
        self.user = mommy.make('profiles.User', _fill_optional=True)
        self.profile = Profile.objects.last()

    def test_if_user_profile_is_created(self):
        self.assertEqual(self.user.id, self.profile.user_id)

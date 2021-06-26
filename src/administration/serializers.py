from rest_framework import serializers
from django.contrib.auth import get_user_model
# Django
from django.core.exceptions import ObjectDoesNotExist

from profiles.models import Profile
from profiles.serializers import UserSerializer


class CandidatesListSerializer(serializers.ModelSerializer):
    user = UserSerializer(get_user_model())
    class Meta:
        model = Profile
        fields = ('id', 'user', 'total_score', 'is_reviewed', 'process_status', 'Address')
        depth = 2
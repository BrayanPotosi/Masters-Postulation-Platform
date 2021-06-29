from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Score

from profiles.models import Profile
from profiles.serializers import UserSerializer

User = get_user_model()

class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = '__all__'


class CandidatesListSerializer(serializers.ModelSerializer):
    user = UserSerializer(User)
    class Meta:
        model = Profile
        fields = ('id', 'user', 'total_score', 'is_reviewed', 'process_status', 'Address')
        depth = 2

class CandidateDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(User)
    class Meta:
        model = Profile
        fields = '__all__'
        depth = 2

class AdminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password','groups', 'user_permissions')
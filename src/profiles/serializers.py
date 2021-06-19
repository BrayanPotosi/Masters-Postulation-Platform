from rest_framework import serializers
from .models import JobStatus


class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobStatus
        exclude = ('updated', 'created')


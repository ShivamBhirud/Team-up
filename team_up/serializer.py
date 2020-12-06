from rest_framework import serializers
from .models import ApplicationStatus


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = ('comments',)
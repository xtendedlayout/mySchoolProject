from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model
from .models import Announcement

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'type', 'created_by', 'created_at', 'attachment']
        read_only_fields = ['created_by', 'created_at']

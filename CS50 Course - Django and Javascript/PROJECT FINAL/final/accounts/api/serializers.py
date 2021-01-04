from rest_framework import serializers

from accounts.models import Profile, User


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        fields = ['user', 'username', 'image', 'bio', 'slug']
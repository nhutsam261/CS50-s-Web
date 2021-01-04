from accounts.models import User, Profile
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from chat.models import Chat
from .serializers import ProfileSerializer



def get_user_profile(username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.filter(user=user)
    return profile


class ProfileListView(ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny, )
    # queryset = Profile.objects.all()

    def get_queryset(self):
        queryset = Profile.objects.all()
        username = self.request.query_params.get('username', None)
        if username is not None:
            profile = get_user_profile(username)
            queryset = profile
        return queryset


class ProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.AllowAny, )


class ProfileCreateView(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ProfileUpdateView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )


class ProfileDeleteView(DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (permissions.IsAuthenticated, )

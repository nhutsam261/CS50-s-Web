from django.urls import path, re_path

from .views import (
    ProfileListView,
    ProfileDetailView,
    ProfileCreateView,
    ProfileUpdateView,
    ProfileDeleteView
)

app_name = 'profile'

urlpatterns = [
    path('', ProfileListView.as_view()),
    path('create/', ProfileCreateView.as_view()),
    path('<pk>', ProfileDetailView.as_view()),
    path('<pk>/update/', ProfileUpdateView.as_view()),
    path('<pk>/delete/', ProfileDeleteView.as_view())
]

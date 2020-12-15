
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.PostListView.as_view(), name="index"),
    path("following/<str:username>", views.FollowingListView.as_view(), name="following"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("users/<slug>/", views.profile, name="profile"),
    path("posts", views.posts, name="posts"),
    path("post", views.post, name="post"),
    path('like/<int:post_id>', views.like, name="like"),
    path('follow/<int:following_user_id>', views.follow, name="follow"),
    path('edit/<int:post_id>', views.edit, name="edit"),
    path('comments/<int:post_id>', views.comments, name="comments"),
]

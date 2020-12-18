
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", auth_views.LoginView.as_view(template_name='network/login.html'), name="login"),
    path("logout", auth_views.LogoutView.as_view(template_name='network/logout.html'), name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("post/<int:post_id>", views.post, name="post"),
    path("like_post/<int:post_id>", views.like_post, name="like_post"),
    path("profile/<slug>", views.profile_view, name="profile_view"),
    path("follow_unfollow/<int:profile_id>", views.follow_unfollow, name="follow_unfollow"),
    path("following_posts", views.following_posts, name="following_posts")
]

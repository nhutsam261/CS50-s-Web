from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("post/<int:post_id>", views.post, name='post'),
    path("like_post/<int:post_id>", views.like, name='like'),
    path("create_post", views.create_post, name='create_post')

]


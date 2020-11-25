from django.contrib import admin
from django.urls import path, include
from . import views
from .views import PostUpdateView, PostListView, UserPostListView, WatchListView, ClosedPostListView, WinPostListView
import notifications.urls
from django.conf.urls import url
urlpatterns=[
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('close/<int:pk>/', views.close_post, name='close-post'),
    path('seen', views.seen, name='seen'),
    path('closed', ClosedPostListView.as_view(), name='closed'),
    path('win', WinPostListView.as_view(), name='win'),
    path('', PostListView.as_view(), name='home'),
    path('post/new/', views.create_post, name='post-create'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),
    path('like/', views.like, name='post-like'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.post_delete, name='post-delete'),
    path('search_posts/', views.search_posts, name='search_posts'),
    path('user_posts/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('watchlist', WatchListView.as_view(), name='watchlist'),
    path('bid', views.bid, name='bid'),
]
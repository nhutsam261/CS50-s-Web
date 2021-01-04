from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

# app_name = "accounts"

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    path('users_list/', views.users_list, name='users_list'),
    path('user/<slug>/', views.profile_view, name='profile_view'),
    path('my-profile/', views.my_profile, name='my_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('friendlist/', views.friend_list, name='friend_list'),
    path('friend-request/send/<int:id>', views.send_friend_request, name='send_friend_request'),
    path('friend-request/cancel/<int:id>', views.cancel_friend_request, name='cancel_friend_request'),
    path('friend-request/accept/<int:id>', views.accept_friend_request, name='accept_friend_request'),
    path('friend-request/reject/<int:id>', views.reject_friend_request, name='reject_friend_request'),
    path('friend/unfriend/<int:id>', views.unfriend, name='unfriend'),

]
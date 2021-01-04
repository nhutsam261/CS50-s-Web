from django.shortcuts import render, get_object_or_404
from .models import Chat
from accounts.models import User, Profile


# Create your views here.
def get_last_10_messages(chatId):
    chat = get_object_or_404(Chat, id=chatId)
    return chat.messages.order_by('-timestamp').all()[:10]

def get_user_contact(username):
    user = get_object_or_404(User, username=username)
    return get_object_or_404(Profile, user=user)

def get_current_chat(chatId):
    return get_object_or_404(Chat, id=chatId)



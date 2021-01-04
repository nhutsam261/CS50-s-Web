from django.db import models
from django.conf import settings
from accounts.models import Profile, User

# Create your models here.
class Message(models.Model):
    author = models.ForeignKey(Profile, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author.user.username

    def last_10_messages():
        return Message.objects.order_by('-timestamp').all()[:10]
    
    def serialize(self):
        return {
            'id': self.id,
            'author': self.author.user.username,
            'content': self.content,
            'timestamp': str(self.timestamp)
        }

class Chat(models.Model):
    participants = models.ManyToManyField(Profile, related_name='chats')
    messages = models.ManyToManyField(Message, blank=True)

    # def last_10_messages(self):
    #     return self.messages.order_by('-timestamp').all()[:10]

    def __str__(self):
        return "{}".format(self.pk) 
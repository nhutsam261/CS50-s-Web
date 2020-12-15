from django.contrib.auth.models import User
from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    slug = AutoSlugField(populate_from='user')
    bio = models.CharField(max_length=255, blank=True)
    
    def __str__(self):
        return str(self.user.username)
    def serialize(self):
        return {
            'user': self.user.username,
            'bio': self.bio,
        }

    def get_absolute_url(self):
        return f"/users/{self.slug}"

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

class Post(models.Model):
    description = models.CharField(max_length = 2048, blank = False, default = 'What are you thinking?')
    date_posted = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', default="")
    def __str__(self):
        return f'{self.description}'
    def serialize(self):
        return {
            'author': self.user.username,
            'description': self.description,
            'date_posted': self.date_posted.strftime("%b %-d %Y, %-I:%M %p"),
            'like': self.likes.count(),
        }
    def format_time(self):
        return self.date_posted.strftime("%b %-d %Y,%-I:%M %p")

class Comments(models.Model):
    post = models.ForeignKey(Post, related_name = 'comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name = 'comments', on_delete=models.CASCADE)
    content = models.CharField(max_length = 2048, blank = True)
    date_commented = models.DateTimeField(default=timezone.now)

    def serialize(self):
        return {
            'user': self.user.username,
            'content': self.content,
            'date_commented': self.date_commented.strftime("%b %-d %Y, %-I:%M %p"),
            }

class Likes(models.Model):
    post = models.ForeignKey(Post, related_name = 'likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name = 'likes', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} liked post {self.post.description}'

class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)

    following_user= models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)

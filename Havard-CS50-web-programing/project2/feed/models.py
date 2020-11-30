from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class Post(models.Model):
    description = models.CharField(max_length=1024, blank=False, default='No Description')
    pic = models.ImageField(upload_to='media/')
    date_posted = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')

    userBid = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='bidpost', null=True, blank=True)

    tags = models.CharField(max_length=100, blank=False, default='Category')
    bid = models.IntegerField(blank=False, default=100)
    nameOfListing = models.CharField(max_length=100, blank=False, default='NEW')
    status = models.IntegerField(blank=False, default=1)
    date_closed = models.DateTimeField(default=timezone.now)
    date_added = models.DateTimeField(default=timezone.now)

    

    def get_user_bid(self):
        if self.userBid is None:
            return False
        return True
    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
 

class Comments(models.Model):
    post = models.ForeignKey(Post, related_name='details', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='details', on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_date = models.DateTimeField(default=timezone.now)

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user} -- {self.post.nameOfListing}"




    
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from autoslug import AutoSlugField


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField("Profile", blank=True, related_name="following")
    slug = AutoSlugField(populate_from='user')

    def get_absolute_url(self):
	    return ("/profile/{}".format(self.slug))


# make a profile as soon as we create the user
def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
	if created:
		try:
			Profile.objects.create(user=instance)
		except:
			pass
        
post_save.connect(post_save_user_model_receiver, sender=User)


class Post(models.Model):
    creator = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=1024)
    createdDate = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'creator': self.creator.id,
            'likes': self.likes.count(),
            'createdDate': self.createdDate.strftime("%b %-d %Y, %-I:%M %p"),
        }
    


class Like(models.Model):
    byProfile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    onPost = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")

    
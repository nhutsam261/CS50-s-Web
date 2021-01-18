from django.contrib.auth.models import User
from django.db import models
from autoslug import AutoSlugField
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name="profile")
    image = models.ImageField(default='./media/default.png', upload_to='profile_pics')
    slug = AutoSlugField(populate_from='user')
    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
        except:
            pass

post_save.connect(post_save_user_model_receiver, sender=settings.AUTH_USER_MODEL)

class Product(models.Model):
    name_product = models.CharField(max_length=2048, blank=False)
    category =  models.CharField(max_length=2048, blank=False)
    date_posted =  models.DateTimeField(default=timezone.now)
    price = models.IntegerField(blank=False)
    images_product = models.ImageField(upload_to='media/')
    amount_of_product = models.IntegerFiled(blank = False)
    description = models.CharField(max_length=4000, blank=False)
    count_sold = models.IntegerField(default=0, verbose_name=_('count sold'))
    status = models.IntegerField(default=100)

    def serialize(self):
         return {
            "id": self.id,
            "name_product": self.name_product,
            "category": self.category,
            "date_posted": self.date_posted,
            "price": self.price,
            "amount_of_product": self.amount_of_product,
            "description": self.description,
            "count_sold": self.count_sold,
            "status":self.status,
        }


class Reviews(modes.Model):
    product = models.ForeignKey(Product, related_name = 'reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name = 'reviews', on_delete=models.CASCADE)
    content = models.CharField(max_length=1024)
    reviewed_date = models.DateTimeField(default=timezone.now)

class Start(models.Model):
    user = model.ForeignKey(User, related_name='start', on_delete=models.CASCADE)
    product = modesl.ForeignKey(Product, related_name='start')

    def __str__(self):
        return f"{self.user} -- {self.product.name_product}

ORDER_STATUS = ((0, 'Started'), (1, 'Done'), (2, 'Error'))

class Order(models.Model):
    user = models.ForeignKey(User, related_name="order", on_delete=models.CASCADE)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, related_name='order_product', on_delete = models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_product', on_delete = models.CASCADE)
    quantity = models.IntegerField(default=1)


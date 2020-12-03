from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Max

from django.utils import timezone



class Auction(models.Model):
    STATUS = [
        ('active', 'active'),
        ('closed', 'closed')
    ]

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    startBid = models.PositiveIntegerField()
    image = models.ImageField(upload_to="images/", blank=True, default='default.png')
    category = models.CharField(max_length=64)
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    createdOn = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=16, choices=STATUS, default='active')


class Bid(models.Model):
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,)
    forAuction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField()

    def clean(self):    
        bids_for_auction = Bid.objects.filter(forAuction=self.forAuction)
        max_price = bids_for_auction.aggregate(Max('price'))['price__max']

        if max_price:
            if (self.price <= max_price):
                raise ValidationError("Cannot bid lower or equal the current price")
        else:
            if self.price <= self.forAuction.startBid:
                raise ValidationError("Cannot bid lower or equal the current price")


class Comment(models.Model):
    onAuction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments", null=True)
    content = models.TextField()
    createdBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    createdOn = models.DateTimeField(auto_now_add=True)

class Watchlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Auction, blank=True)



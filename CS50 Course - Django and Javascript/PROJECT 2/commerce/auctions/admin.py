from django.contrib import admin
from .models import Auction, Bid, Comment, Watchlist


class AuctionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'startBid',
                    'image', 'category', 'createdBy', 'status')

class BidAdmin(admin.ModelAdmin):
    list_display = ('id', 'createdBy', 'forAuction', 'price')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'createdBy', 'content', 'createdOn')


# Register your models here.
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Watchlist)



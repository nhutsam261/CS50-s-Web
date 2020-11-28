from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .form import AuctionForm, BidForm, CommentForm

from .models import Auction, Bid, Comment
from django.db.models import Max
from collections import defaultdict




def index(request):
    auctions = Auction.objects.filter(status='active')    
    max_bids_dict = {}
    for auction in auctions:
       max_bids_dict[auction] = Bid.objects.filter(forAuction=auction).order_by('-price')[0].price if Bid.objects.filter(forAuction=auction).order_by('-price') else None
    print(max_bids_dict)

    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "max_bids_dict": max_bids_dict
    })


@login_required
def create(request):
    if request.method == "POST":
        f = AuctionForm(request.POST, request.FILES)
        if f.is_valid():
            new_auction = f.save()
            new_auction.createdBy = request.user
            new_auction.save(update_fields=['createdBy'])
            return HttpResponseRedirect(reverse("home"))
        else:
            return  render(request, "auctions/create.html", {
                        "create_form": f
                    })
    else:        
        return render(request, "auctions/create.html", {
            "create_form": AuctionForm()
        })



# Details on one listing and for bidding
def listing(request, num_id):
    # Check if user is loged in
    auction = Auction.objects.get(pk=num_id)
    max_bid = Bid.objects.filter(forAuction=auction).order_by('-price') # the max bid on the auction
    cmts = auction.comments.all()  
    
    if (request.method == "POST"):
        newBid = Bid(createdBy=request.user, forAuction=auction)
        f = BidForm(request.POST, instance=newBid)
        if f.is_valid():
            bid = f.save()
            return HttpResponseRedirect(reverse("listing", args=[num_id]))
        else:
            return render(request, "auctions/product.html", {
                "auction": auction,
                "bid_form": f,
                "bids_for_auction": Bid.objects.filter(forAuction=auction),
                "max_bid": max_bid[0] if max_bid else None,
                "comments": cmts,
                "comment_form": CommentForm()
                                        
            })

    return render(request, "auctions/product.html", {
        "auction": auction,
        "bid_form": BidForm(),
        "bids_for_auction": Bid.objects.filter(forAuction=auction),
        "max_bid": max_bid[0] if max_bid else None,
        "comments": cmts,
        "comment_form": CommentForm()
    
    })


# For closing a listing
def close(request, num_id = -1):
    closed_auctions = Auction.objects.filter(status='closed')

    max_bids_dict = {}
    for auction in closed_auctions:
       max_bids_dict[auction] = Bid.objects.filter(forAuction=auction).order_by('-price')[0].price if Bid.objects.filter(forAuction=auction).order_by('-price') else None
    
    if num_id != -1:
        auctionToBeClosed = Auction.objects.get(pk=num_id)
        auctionToBeClosed.status = 'closed'
        auctionToBeClosed.save()
        return HttpResponseRedirect(reverse('close_view')) # back to closed listings template


    return render(request, "auctions/closed.html", {
        "auctions": closed_auctions,
        "max_bids_dict": max_bids_dict

    })


# For commenting on a listing page
@login_required
def comment(request, num_id):
    if request.method == "POST":
        f = CommentForm(request.POST)
        if f.is_valid():
            content = f.cleaned_data["content"]
            cmt = Comment.objects.create(createdBy=request.user, 
                    onAuction=Auction.objects.get(pk=num_id), content= content)
        
    return HttpResponseRedirect(reverse("listing", args=[num_id])) 
    
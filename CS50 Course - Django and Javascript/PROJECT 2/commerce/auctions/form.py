from django.forms import ModelForm
from .models import Auction, Bid, Comment
from django import forms

class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description', 'startBid',
                    'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title', 'size': '50%'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description', 'size': '50%', "rows":5, "cols":20}),
            'startBid': forms.NumberInput(attrs={'placeholder': 'Price', 'size': '50%'}),
            'image': forms.FileInput(),
            'category': forms.TextInput(attrs={'placeholder': 'Category', 'size': '50%'})

        }


class BidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['price']
        widgets = {
            'price': forms.NumberInput(attrs={'placeholder': 'Bid'})
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
           'content' : '',
        }

        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Leave your comment!',
                'rows': 4,
                'cols': 50,
                # 'padding-left': '20px'
            })
        }
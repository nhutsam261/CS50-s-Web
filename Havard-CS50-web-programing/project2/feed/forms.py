from django import forms
from .models import Comments, Post

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'pic', 'tags', 'bid', 'nameOfListing']
        widgets = {
            'description': forms.Textarea(attrs={'rows':15, 'cols':70,}),}
class NewCommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        fields = ['comment']
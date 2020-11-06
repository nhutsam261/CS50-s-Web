from django import forms
from . import util


class SearchForm(forms.Form):
    keyword = forms.CharField(label='', widget= forms.TextInput(attrs={
                        'placeholder':'Search Encyclopedia', 'class': 'search'}),
                        required=False)

class CreatePageForm(forms.Form):
    title = forms.CharField(label="Title", required=True, widget=forms.TextInput(
        attrs={'class':'col-sm-12', 
            'id': 'title-area'}
    ))

    content = forms.CharField(label="Markdown content", required=True, widget=forms.Textarea(
        attrs={'class': 'col-sm-12', 
                'id': 'content-area',}
    ))

class EditPageForm(forms.Form):
    content = forms.CharField(label="Markdown content", required=True, widget=forms.Textarea(
            attrs={'class': 'col-sm-12', 
                'id': 'content-area',}
            ))
       
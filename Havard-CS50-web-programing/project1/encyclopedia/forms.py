from django import forms

class NewSearchForm(forms.Form):
    search = forms.CharField(label='', required= False,
    widget= forms.TextInput
    (attrs={'placeholder':'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    pagename = forms.CharField(label='', required=True, widget = forms.TextInput(attrs={'placeholder': 'Title', 'class': 'col-sm-6'}))

    body = forms.CharField(label='', required=True, widget = forms.Textarea(attrs={'placeholder': 'paste markdown here ✨', 'class': 'col-sm-10', 'style' : 'top:2rem; margin-bottom:50px;'}))

class EditPageForm(forms.Form):
    pagename = forms.CharField(label='Title ', disabled=False, required=False, widget=forms.HiddenInput(attrs={'class':'col-sm-12', 'style':'bottom:1rem'}))

    body = forms.CharField(label='Markdown Content', required=False, widget = forms.Textarea(attrs = {'rows':'2', 'cols': '3', 'placeholder': 'Content', 'class':'col-sm-12', 'style':'top:2rem; margin-bottom:50px'}))









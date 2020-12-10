from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Email


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['email', 'password1', 'password2']


class UserLogInForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields =['email', 'password']

		widgets = {
			'password': forms.TextInput(attrs={
				'type':'password'
				}),

		}


class ComposeForm(forms.ModelForm):
	class Meta:
		model = Email
		fields = ['sender', 'recipients', 'subject', 'body']
		widgets = {
			'recipient': forms.EmailInput(attrs={
				'class': 'form-control',
				'id': "compose-recipients" }),
			
			'subject': forms.TextInput(attrs={
				'class': 'form-control',
				'id': "compose-subject",
				'placeholder': "Subject"
			}),

			'body': forms.Textarea(attrs={
				'class': 'form-control',
				'id': "compose-body",
				'placeholder': "Body",
				'min-height': '400px'
			})


		}


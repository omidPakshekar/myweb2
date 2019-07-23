from django import forms
from django.contrib.auth.models import User
from .models import Profile
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2= forms.CharField(label='password', widget=forms.PasswordInput) 

    class Meta:
        model = User  
        fields = ('username', 'first_name', 'email')

class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('date_of_birth', 'photo')

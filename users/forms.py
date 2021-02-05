from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateFrom(forms.ModelForm):
    
    class Meta:
        model = Profile
        exclude = ['user',]

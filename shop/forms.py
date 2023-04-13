from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class UserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'user_name'}))
    email=forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'sample@gmail.com'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'********'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'********'}))
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']

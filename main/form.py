from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import MyUser
from django import forms


class RegisterUserForm(UserCreationForm):
    username=forms.CharField(label='Login', widget=forms.TextInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Wprowadź hasło jeszcze raz', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    krs = forms.CharField(label='Wprowadź numer KRS spółki', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model= MyUser
        fields=('username', 'password1', 'password2','krs')


class LoginUserForm(AuthenticationForm):
    username=forms.CharField(label='Login', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

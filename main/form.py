from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import MyUser
from django import forms


class RegisterUserForm(UserCreationForm):
    username=forms.CharField(label='Login', widget=forms.TextInput(attrs={'class':'form-input'}))
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Wprowadź hasło jeszcze raz', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    krs = forms.CharField(label='Wprowadź numer KRS spółki', widget=forms.TextInput(attrs={'class': 'form-input'}))
    B_account_number = forms.CharField(label='Wprowadź numer konta bankowego spółki', widget=forms.TextInput(attrs={'class': 'form-input'}))
    Bank_name = forms.CharField(label='Wprowadź nazwę banku', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model= MyUser
        fields=('username', 'password1', 'password2','krs', 'B_account_number', 'Bank_name')


class LoginUserForm(AuthenticationForm):
    username=forms.CharField(label='Login', widget=forms.TextInput(attrs={'class':'form-input'}))
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

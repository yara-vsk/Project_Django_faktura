from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .form import RegisterUserForm, LoginUserForm


def index(request):
    return render(request,'main/index.html')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = '/'


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('/')
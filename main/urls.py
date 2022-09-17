from django.contrib import admin
from django.urls import path, include
from .views import index, RegisterUser, LoginUser, logout_user


urlpatterns = [
    path('', index,name='home'),
    path('register/', RegisterUser.as_view()),
    path('login/', LoginUser.as_view()),
    path('logout/', logout_user),
]
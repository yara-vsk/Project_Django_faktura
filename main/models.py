
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class MyUser(AbstractUser):
    krs = models.CharField(unique=True, max_length=10)
    B_account_number = models.CharField( max_length=45)
    Bank_name = models.CharField( max_length=45)

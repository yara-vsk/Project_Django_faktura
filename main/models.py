
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class MyUser(AbstractUser):
    krs = models.CharField(unique=True, max_length=10)

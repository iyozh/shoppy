from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from applications.auth_app.managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    is_confirmed = models.BooleanField(default=False)
    code = models.CharField(max_length=255, null=False, blank=False)
    USERNAME_FIELD = 'email'

    objects = UserManager()

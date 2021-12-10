from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users', blank=True)
    age = models.PositiveSmallIntegerField(default=18, verbose_name='Age')


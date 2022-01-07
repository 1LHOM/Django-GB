import pytz
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users', blank=True)
    age = models.PositiveSmallIntegerField(default=18, verbose_name='Age')

    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expires = models.DateTimeField(blank=True, null=True)

    def is_activation_key_expired(self):
        if datetime.now(pytz.timezone(settings.TIME_ZONE)) <= self.activation_key_expires + timedelta(hours=48):
            return False
        else:
            return True

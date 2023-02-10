from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Почта', unique=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20)
    avatar = models.ImageField(verbose_name='Аватарка', upload_to='users/')
    country = models.CharField(verbose_name='Страна', max_length=30)
    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
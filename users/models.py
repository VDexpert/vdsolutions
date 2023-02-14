from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    MAN = 'мужской'
    WOMAN = 'женский'
    GENDERS = (
        (MAN, 'мужской'),
        (WOMAN, 'женский')
    )

    username = None
    email = models.EmailField(verbose_name='Почта', unique=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20, **NULLABLE)
    avatar = models.ImageField(verbose_name='Аватарка', upload_to='users/', help_text=f'рекомендуемый размер 600*600', **NULLABLE)
    country = models.CharField(verbose_name='Страна', max_length=30, **NULLABLE)
    email_verify = models.BooleanField(default=False)
    trials_update_range_prod = models.IntegerField(verbose_name='Кол-во апдейта ранжирования продукта', default=10)
    stack = models.CharField(verbose_name='Опишите Ваш стэк', max_length=80, **NULLABLE, help_text='максимальное количество символов - 80')
    gender = models.CharField(verbose_name='Пол', choices=GENDERS, max_length=10, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
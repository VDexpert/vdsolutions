from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    BANNED_TRUE = 'заблокировано модератором'
    BANNED_FALSE = 'одобрено модератором'
    BANNED_STATUSES = (
        (BANNED_TRUE, 'ДА'),
        (BANNED_FALSE, 'НЕТ')
    )

    user = models.ForeignKey(User, verbose_name='Продавец', on_delete=models.CASCADE, **NULLABLE)
    product_name = models.CharField(max_length=70, verbose_name='Наименование', db_index=True, unique=True)
    slug = models.SlugField(max_length=70, verbose_name='URL',  db_index=True, unique=True, null=True)
    picture = models.ImageField(verbose_name='Фото', upload_to='products/', **NULLABLE)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', db_index=True)
    unit_price = models.CharField(verbose_name='Цена', max_length=10)
    create_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    change_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    banned = models.CharField(choices=BANNED_STATUSES, default=BANNED_FALSE, max_length=30, verbose_name='Забанить продукт?')
    description = models.TextField(verbose_name='Полное описание')
    meta_title = models.CharField(verbose_name='Метатег title', max_length=70, **NULLABLE)
    meta_description = models.CharField(verbose_name='Метатег description', max_length=300, **NULLABLE)

    class Meta():
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        permissions = [
            ('moderating_products', 'Банить и редактировать все продукты'),
        ]

    def get_absolute_url(self):
        return reverse_lazy('catalog:product_detail', kwargs={'cat_slug': self.category.slug, 'prod_slug': self.slug})

    def __str__(self):
        return f'{self.product_name}, {self.slug}, {self.unit_price}, {self.category}'


class Version(models.Model):
    STATUS_ACTIVE = 'активно'
    STATUS_INACTIVE = 'неактивно'
    STATUSES = (
        (STATUS_ACTIVE, 'ДА'),
        (STATUS_INACTIVE, 'НЕТ')
    )

    value = models.CharField(verbose_name='Номер версии', max_length=10)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    description = models.CharField(verbose_name='Улучшения версии', max_length=250)
    status = models.CharField(verbose_name='Версия активная?', choices=STATUSES, default=STATUS_INACTIVE, max_length=10)

    def __str__(self):
        return f'{self.value}, {self.product}, {self.description}, {self.status}'

    class Meta():
        verbose_name = 'версия'
        verbose_name_plural = 'версии'


class Category(models.Model):
    category_name = models.CharField(max_length=50, verbose_name='Наименование', db_index=True, unique=True)
    slug = models.SlugField(max_length=70, verbose_name='URL', db_index=True, unique=True, **NULLABLE)
    none_products = models.CharField(verbose_name='Категория пустая?', default='true', max_length=10)
    none_posts = models.CharField(verbose_name='Категория пустая?', default='true', max_length=10)

    category_h1_for_products = models.CharField(verbose_name='Заголовк H1 для продуктов', max_length=70, **NULLABLE)
    annotation_for_products = models.CharField(verbose_name='Аннотация для продуктов', max_length=120, **NULLABLE)
    description_for_products = models.TextField(verbose_name='Полное описание для продуктов', **NULLABLE)
    meta_title_for_products = models.CharField(verbose_name='Title для продуктов', max_length=70, **NULLABLE)
    meta_description_for_products = models.CharField(verbose_name='Description для продуктов', max_length=300, **NULLABLE)
    keywords_for_products = models.CharField(verbose_name='Keywords для продуктов', max_length=150, **NULLABLE)

    category_h1_for_posts = models.CharField(verbose_name='Заголовк H1 для блога', max_length=70, **NULLABLE)
    annotation_for_posts = models.CharField(verbose_name='Аннотация для блога', max_length=120, **NULLABLE)
    description_for_posts = models.TextField(verbose_name='Полное описание для блога', **NULLABLE)
    meta_title_for_posts = models.CharField(verbose_name='Title для блога', max_length=70, **NULLABLE)
    meta_description_for_posts = models.CharField(verbose_name='Description для блога', max_length=300,**NULLABLE)
    keywords_for_posts = models.CharField(verbose_name='Keywords для блога', max_length=150, **NULLABLE)

    class Meta():
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

        permissions = [
            ('management_category', 'Редактировать контент категорий'),
        ]

    def get_absolute_url(self):
        return reverse_lazy('catalog:category_with_products', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.category_name}'


class Post(models.Model):
    STATUS_ACTIVE = 'опубликовано'
    STATUS_INACTIVE = 'не опубликовано'
    STATUSES = (
        (STATUS_ACTIVE, 'ДА'),
        (STATUS_INACTIVE, 'НЕТ')
    )

    BANNED_TRUE = 'заблокировано модератором'
    BANNED_FALSE = 'одобрено модератором'
    BANNED_STATUSES = (
        (BANNED_TRUE, 'ДА'),
        (BANNED_FALSE, 'НЕТ')
    )

    user = models.ForeignKey(User, verbose_name='Автор (продавец)', on_delete=models.CASCADE, **NULLABLE)
    title = models.CharField(max_length=300, verbose_name='Заголовок', db_index=True, unique=True)
    slug = models.SlugField(max_length=150, verbose_name='URL',  db_index=True, unique=True, null=True)
    content = models.TextField(verbose_name='Содержание')
    picture = models.ImageField(verbose_name='Фото', upload_to='posts/', **NULLABLE)
    create_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    change_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    status = models.CharField(choices=STATUSES, default=STATUS_ACTIVE, max_length=20, verbose_name='Публиковать?')
    category = models.ForeignKey('Category', verbose_name='Категория', db_index=True, on_delete=models.PROTECT, **NULLABLE)
    meta_title = models.CharField(verbose_name='Метатег title для SEO', max_length=70, **NULLABLE)
    meta_description = models.CharField(verbose_name='Метатег description для SEO', max_length=300, **NULLABLE)
    banned = models.CharField(choices=BANNED_STATUSES, default=BANNED_FALSE, max_length=30, verbose_name='Забанить пост?')

    class Meta():
        verbose_name = 'публикация'
        verbose_name_plural = 'публикации'

        permissions = [
            ('management_posts', 'Редактировать контент блога и банить статьи'),
        ]

    def __str__(self):
        return f'{self.title},{self.slug}, {self.create_at}, {self.change_at}, {self.count_views}, {self.status}'

    def get_absolute_url(self):
        return reverse_lazy('catalog:post_detail', kwargs={'post_slug': self.slug, 'cat_slug': self.category.slug})
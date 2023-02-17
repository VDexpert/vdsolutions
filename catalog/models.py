from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy
from users.models import User
from tinymce import models as tinymce_models

NULLABLE = {'blank': True, 'null': True}


class Home(models.Model):
    home_h1 = models.CharField(max_length=100, verbose_name='Заголовок',  help_text='До 100 символов')
    home_annotation = models.CharField(max_length=150, verbose_name='Аннотация', help_text='До 150 символов')
    title = models.CharField(max_length=70, verbose_name='Метатэг Title', help_text='До 70 символов')
    description = tinymce_models.HTMLField(verbose_name='Содержание', **NULLABLE)
    meta_description = models.CharField(verbose_name='Метатэг description', max_length=300, **NULLABLE, help_text='До 300 символов')
    meta_keywords = models.CharField(max_length=150, verbose_name='Метатег Keywords', **NULLABLE, help_text='До 150 символов')

    class Meta():
        verbose_name = 'Главная страница'
        verbose_name_plural = 'Главная страница'


class Blog(models.Model):
    blog_h1 = models.CharField(max_length=100, verbose_name='Заголовок', **NULLABLE,  help_text='До 100 символов')
    blog_annotation = models.CharField(max_length=150, verbose_name='Аннотация', **NULLABLE, help_text='До 150 символов')
    title = models.CharField(max_length=70, verbose_name='Метатэг Title',  **NULLABLE,  help_text='До 70 символов')
    description = tinymce_models.HTMLField(verbose_name='Содержание',  **NULLABLE)
    meta_description = models.CharField(verbose_name='Метатэг Description', max_length=300, **NULLABLE, help_text='До 300 символов')
    meta_keywords = models.CharField(max_length=150, verbose_name='Метатег Keywords', **NULLABLE, help_text='До 150 символов')

    class Meta():
        verbose_name = 'Блог'
        verbose_name_plural = 'Блог'


class Contacts(models.Model):
    contacts_h1 = models.CharField(max_length=100, verbose_name='Заголовок', **NULLABLE,  help_text='До 100 символов')
    title = models.CharField(max_length=70, verbose_name='Метатэг Title', **NULLABLE,  help_text='До 70 символов')
    official_company_name = models.CharField(max_length=30, verbose_name='Юридическое название', **NULLABLE,  help_text='До 30 символов')
    country = models.CharField(max_length=20, verbose_name='Страна', **NULLABLE,  help_text='До 20 символов')
    itin = models.CharField(max_length=20, verbose_name='ИНН', **NULLABLE,  help_text='До 20 символов')
    address = models.CharField(max_length=50, verbose_name='Адрес', **NULLABLE,  help_text='До 50 символов')
    phone = models.CharField(max_length=30, verbose_name='Телефон', **NULLABLE,  help_text='До 30 символов')
    email = models.CharField(max_length=20, verbose_name='Email', **NULLABLE,  help_text='До 20 символов')
    meta_description = models.CharField(verbose_name='Метатэг Description', max_length=300, **NULLABLE,
                                        help_text='До 300 символов')
    meta_keywords = models.CharField(max_length=150, verbose_name='Метатег Keywords', **NULLABLE,
                                     help_text='До 150 символов')

    class Meta():
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'


class Product(models.Model):
    STATUS_ACTIVE = 'опубликовано'
    STATUS_INACTIVE = 'не опубликовано'
    STATUSES = (
        (STATUS_ACTIVE, 'ДА'),
        (STATUS_INACTIVE, 'НЕТ')
    )

    BANNED_TRUE = 'заблокировано модератором'
    BANNED_FALSE = 'одобрено модератором'
    BANNED_STATUSES = (
        (BANNED_TRUE, 'ЗАБАНИТЬ'),
        (BANNED_FALSE, 'РАЗБАНИТЬ')
    )

    CONFIRM_TRUE = 'true'
    CONFIRM_FALSE = 'false'
    CONFIRMS = (
        (CONFIRM_TRUE, 'ДА'),
        (CONFIRM_FALSE, 'НЕТ')
    )

    user = models.ForeignKey(User, verbose_name='Продавец', on_delete=models.CASCADE, **NULLABLE)
    product_name = models.CharField(max_length=90, verbose_name='Наименование', db_index=True, unique=True,
                                    help_text='До 90 символов')
    slug = models.SlugField(max_length=90, verbose_name='URL',  db_index=True, unique=True, null=True)
    picture = models.ImageField(verbose_name='Фото', upload_to='products/', **NULLABLE, help_text='рекомендуемый размер - 2000*1000')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', db_index=True)
    unit_price = models.CharField(verbose_name='Цена', max_length=10)
    status = models.CharField(choices=STATUSES, default=STATUS_ACTIVE, max_length=20, verbose_name='Публиковать?')
    banned = models.CharField(choices=BANNED_STATUSES, default=BANNED_FALSE, max_length=30, verbose_name='Забанить продукт?')
    prod_annotation = models.CharField(max_length=150, verbose_name='Аннотация', **NULLABLE)
    description = tinymce_models.HTMLField(verbose_name='Полное описание', **NULLABLE)
    confirm_update_range = models.CharField(choices=CONFIRMS, default=CONFIRM_TRUE, verbose_name='Поднять продукт в ТОП?', max_length=10)
    create_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    change_at = models.DateTimeField(verbose_name='Дата изменения', auto_now=True)

    change_range_prod = models.DateTimeField(verbose_name='Рейтинг изменен', **NULLABLE)
    absolute_top = models.IntegerField(verbose_name='Позиция в топе', default=0, **NULLABLE)

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

    value = models.CharField(verbose_name='Номер', max_length=10)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='Продукт')
    description = models.CharField(verbose_name='Улучшения', max_length=250,  help_text='До 250 символов')
    status = models.CharField(verbose_name='Релиз?', choices=STATUSES, default=STATUS_INACTIVE, max_length=10)

    def __str__(self):
        return f'{self.value}, {self.product}, {self.description}, {self.status}'

    class Meta():
        verbose_name = 'версия'
        verbose_name_plural = 'версии'


class Category(models.Model):
    category_name = models.CharField(max_length=30, verbose_name='Наименование', db_index=True, unique=True,
                                     help_text='Выбирайте наименование тщательно - от него формируется ссылка и его нельзя будет изменить, до 30 символов')
    slug = models.SlugField(max_length=70, verbose_name='URL', db_index=True, unique=True, **NULLABLE)
    add_new_prod = models.DateTimeField(verbose_name='Дата добавления последнего продукта', **NULLABLE)

    category_h1_for_products = models.CharField(verbose_name='Заголовк H1 для продуктов', max_length=70, **NULLABLE,
                                                help_text='До 70 символов')
    annotation_for_products = models.CharField(verbose_name='Аннотация для продуктов', max_length=200, **NULLABLE,
                                               help_text='До 200 символов',)
    description_for_products = tinymce_models.HTMLField(verbose_name='Полное описание для продуктов', **NULLABLE)
    meta_title_for_products = models.CharField(verbose_name='Title для продуктов', max_length=70, **NULLABLE,
                                               help_text='До 70 символов')
    meta_description_for_products = models.CharField(verbose_name='Description для продуктов', max_length=300, **NULLABLE,
                                                     help_text='До 300 символов')
    keywords_for_products = models.CharField(verbose_name='Keywords для продуктов', max_length=150, **NULLABLE,
                                             help_text='До 150 символов')

    category_h1_for_posts = models.CharField(verbose_name='Заголовк H1 для блога', max_length=70, **NULLABLE,
                                             help_text='До 70 символов')
    annotation_for_posts = models.CharField(verbose_name='Аннотация для блога', max_length=200, **NULLABLE,
                                            help_text='До 200 символов')
    description_for_posts = tinymce_models.HTMLField(verbose_name='Полное описание для блога', **NULLABLE)
    meta_title_for_posts = models.CharField(verbose_name='Title для блога', max_length=70, **NULLABLE,
                                            help_text='До 70 символов')
    meta_description_for_posts = models.CharField(verbose_name='Description для блога', max_length=300,**NULLABLE,
                                                  help_text='До 300 символов')
    keywords_for_posts = models.CharField(verbose_name='Keywords для блога', max_length=150, **NULLABLE,
                                          help_text='До 150 символов')

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
        (BANNED_TRUE, 'ЗАБАНИТЬ'),
        (BANNED_FALSE, 'РАЗБАНИТЬ')
    )

    user = models.ForeignKey(User, verbose_name='Автор (продавец)', on_delete=models.CASCADE, **NULLABLE)
    title = models.CharField(max_length=100, verbose_name='Заголовок', db_index=True, unique=True,  help_text='До 100 символов')
    slug = models.SlugField(max_length=100, verbose_name='URL',  db_index=True, unique=True, null=True)
    content = tinymce_models.HTMLField(verbose_name='Содержание', **NULLABLE)
    picture = models.ImageField(verbose_name='Фото', upload_to='posts/', **NULLABLE, help_text='рекомендуемый размер - 2000*1000')
    create_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    change_at = models.DateTimeField(verbose_name='Дата изменения', **NULLABLE)
    count_views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    status = models.CharField(choices=STATUSES, default=STATUS_ACTIVE, max_length=20, verbose_name='Публиковать?')
    category = models.ForeignKey('Category', verbose_name='Категория', db_index=True, on_delete=models.PROTECT, **NULLABLE)
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
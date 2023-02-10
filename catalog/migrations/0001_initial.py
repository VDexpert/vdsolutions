# Generated by Django 4.1.6 on 2023-02-10 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(db_index=True, max_length=50, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(blank=True, max_length=70, null=True, unique=True, verbose_name='URL')),
                ('none_products', models.CharField(default='true', max_length=10, verbose_name='Категория пустая?')),
                ('none_posts', models.CharField(default='true', max_length=10, verbose_name='Категория пустая?')),
                ('category_h1_for_products', models.CharField(blank=True, max_length=70, null=True, verbose_name='Заголовк H1 для продуктов')),
                ('annotation_for_products', models.CharField(blank=True, max_length=120, null=True, verbose_name='Аннотация для продуктов')),
                ('description_for_products', models.TextField(blank=True, null=True, verbose_name='Полное описание для продуктов')),
                ('meta_title_for_products', models.CharField(blank=True, max_length=70, null=True, verbose_name='Title для продуктов')),
                ('meta_description_for_products', models.CharField(blank=True, max_length=300, null=True, verbose_name='Description для продуктов')),
                ('keywords_for_products', models.CharField(blank=True, max_length=150, null=True, verbose_name='Keywords для продуктов')),
                ('category_h1_for_posts', models.CharField(blank=True, max_length=70, null=True, verbose_name='Заголовк H1 для блога')),
                ('annotation_for_posts', models.CharField(blank=True, max_length=120, null=True, verbose_name='Аннотация для блога')),
                ('description_for_posts', models.TextField(blank=True, null=True, verbose_name='Полное описание для блога')),
                ('meta_title_for_posts', models.CharField(blank=True, max_length=70, null=True, verbose_name='Title для блога')),
                ('meta_description_for_posts', models.CharField(blank=True, max_length=300, null=True, verbose_name='Description для блога')),
                ('keywords_for_posts', models.CharField(blank=True, max_length=150, null=True, verbose_name='Keywords для блога')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
                'permissions': [('management_category', 'Редактировать контент категорий')],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(db_index=True, max_length=70, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=70, null=True, unique=True, verbose_name='URL')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Фото')),
                ('unit_price', models.CharField(max_length=10, verbose_name='Цена')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('change_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('banned', models.CharField(choices=[('заблокировано модератором', 'ДА'), ('одобрено модератором', 'НЕТ')], default='одобрено модератором', max_length=30, verbose_name='Забанить продукт?')),
                ('description', models.TextField(verbose_name='Полное описание')),
                ('meta_title', models.CharField(blank=True, max_length=70, null=True, verbose_name='Метатег title')),
                ('meta_description', models.CharField(blank=True, max_length=300, null=True, verbose_name='Метатег description')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
                'permissions': [('moderating_products', 'Банить и редактировать все продукты')],
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=10, verbose_name='Номер версии')),
                ('description', models.CharField(max_length=250, verbose_name='Улучшения версии')),
                ('status', models.CharField(choices=[('активно', 'ДА'), ('неактивно', 'НЕТ')], default='неактивно', max_length=10, verbose_name='Версия активная?')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'версия',
                'verbose_name_plural': 'версии',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=300, unique=True, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=150, null=True, unique=True, verbose_name='URL')),
                ('content', models.TextField(verbose_name='Содержание')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='posts/', verbose_name='Фото')),
                ('create_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('change_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('count_views', models.IntegerField(default=0, verbose_name='Количество просмотров')),
                ('status', models.CharField(choices=[('опубликовано', 'ДА'), ('не опубликовано', 'НЕТ')], default='опубликовано', max_length=20, verbose_name='Публиковать?')),
                ('meta_title', models.CharField(blank=True, max_length=70, null=True, verbose_name='Метатег title для SEO')),
                ('meta_description', models.CharField(blank=True, max_length=300, null=True, verbose_name='Метатег description для SEO')),
                ('banned', models.CharField(choices=[('заблокировано модератором', 'ДА'), ('одобрено модератором', 'НЕТ')], default='одобрено модератором', max_length=30, verbose_name='Забанить пост?')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='catalog.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'публикация',
                'verbose_name_plural': 'публикации',
                'permissions': [('management_posts', 'Редактировать контент блога и банить статьи')],
            },
        ),
    ]

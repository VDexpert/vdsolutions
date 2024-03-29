# Generated by Django 4.1.6 on 2023-02-14 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stack',
            field=models.CharField(blank=True, help_text='максимальное количество символов - 80', max_length=80, null=True, verbose_name='Опишите Ваш стэк'),
        ),
        migrations.AddField(
            model_name='user',
            name='trials_update_range_prod',
            field=models.IntegerField(default=10, verbose_name='Кол-во апдейта ранжирования продукта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='рекомендуемый размер 300*300', null=True, upload_to='users/', verbose_name='Аватарка'),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон'),
        ),
    ]

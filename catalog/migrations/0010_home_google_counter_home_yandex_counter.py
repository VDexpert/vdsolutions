# Generated by Django 4.1.7 on 2023-03-13 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0009_alter_contacts_email_alter_version_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='home',
            name='google_counter',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Счетчик Google Analytics'),
        ),
        migrations.AddField(
            model_name='home',
            name='yandex_counter',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='Счетчик Яндекс-Метрика'),
        ),
    ]

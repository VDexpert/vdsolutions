# Generated by Django 4.1.6 on 2023-02-14 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_stack_user_trials_update_range_prod_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('мужской', 'мужской'), ('женский', 'женский')], max_length=10, null=True, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='рекомендуемый размер 600*600', null=True, upload_to='users/', verbose_name='Аватарка'),
        ),
    ]

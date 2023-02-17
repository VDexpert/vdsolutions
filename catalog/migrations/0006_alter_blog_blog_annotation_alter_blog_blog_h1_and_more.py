# Generated by Django 4.1.6 on 2023-02-16 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_alter_post_content_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='blog_annotation',
            field=models.CharField(blank=True, help_text='До 150 символов', max_length=150, null=True, verbose_name='Аннотация'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='blog_h1',
            field=models.CharField(blank=True, help_text='До 100 символов', max_length=100, null=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='meta_description',
            field=models.CharField(blank=True, help_text='До 300 символов', max_length=300, null=True, verbose_name='Метатэг Description'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='meta_keywords',
            field=models.CharField(blank=True, help_text='До 150 символов', max_length=150, null=True, verbose_name='Метатег Keywords'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(blank=True, help_text='До 70 символов', max_length=70, null=True, verbose_name='Метатэг Title'),
        ),
        migrations.AlterField(
            model_name='category',
            name='annotation_for_posts',
            field=models.CharField(blank=True, help_text='До 200 символов', max_length=200, null=True, verbose_name='Аннотация для блога'),
        ),
        migrations.AlterField(
            model_name='category',
            name='annotation_for_products',
            field=models.CharField(blank=True, help_text='До 200 символов', max_length=200, null=True, verbose_name='Аннотация для продуктов'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_h1_for_posts',
            field=models.CharField(blank=True, help_text='До 70 символов', max_length=70, null=True, verbose_name='Заголовк H1 для блога'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_h1_for_products',
            field=models.CharField(blank=True, help_text='До 70 символов', max_length=70, null=True, verbose_name='Заголовк H1 для продуктов'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(db_index=True, help_text='Выбирайте наименование тщательно - от него формируется ссылка и его нельзя будет изменить, до 30 символов', max_length=30, unique=True, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='category',
            name='keywords_for_posts',
            field=models.CharField(blank=True, help_text='До 150 символов', max_length=150, null=True, verbose_name='Keywords для блога'),
        ),
        migrations.AlterField(
            model_name='category',
            name='keywords_for_products',
            field=models.CharField(blank=True, help_text='До 150 символов', max_length=150, null=True, verbose_name='Keywords для продуктов'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description_for_posts',
            field=models.CharField(blank=True, help_text='До 300 символов', max_length=300, null=True, verbose_name='Description для блога'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_description_for_products',
            field=models.CharField(blank=True, help_text='До 300 символов', max_length=300, null=True, verbose_name='Description для продуктов'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title_for_posts',
            field=models.CharField(blank=True, help_text='До 70 символов', max_length=70, null=True, verbose_name='Title для блога'),
        ),
        migrations.AlterField(
            model_name='category',
            name='meta_title_for_products',
            field=models.CharField(blank=True, help_text='До 70 символов', max_length=70, null=True, verbose_name='Title для продуктов'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='address',
            field=models.CharField(blank=True, help_text='До 50 символов', max_length=50, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='contacts_h1',
            field=models.CharField(blank=True, help_text='До 100 символов', max_length=100, null=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='country',
            field=models.CharField(blank=True, help_text='До 20 символов', max_length=20, null=True, verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='email',
            field=models.CharField(blank=True, help_text='До 20 символов', max_length=20, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='itin',
            field=models.CharField(blank=True, help_text='До 20 символов', max_length=20, null=True, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='meta_description',
            field=models.CharField(blank=True, help_text='До 300 символов', max_length=300, null=True, verbose_name='Метатэг Description'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='meta_keywords',
            field=models.CharField(blank=True, help_text='До 150 символов', max_length=150, null=True, verbose_name='Метатег Keywords'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='official_company_name',
            field=models.CharField(blank=True, help_text='До 30 символов', max_length=30, null=True, verbose_name='Юридическое название'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='phone',
            field=models.CharField(blank=True, help_text='До 30 символов', max_length=30, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='title',
            field=models.CharField(blank=True, help_text='До 70 символов', max_length=70, null=True, verbose_name='Метатэг Title'),
        ),
        migrations.AlterField(
            model_name='home',
            name='home_annotation',
            field=models.CharField(help_text='До 150 символов', max_length=150, verbose_name='Аннотация'),
        ),
        migrations.AlterField(
            model_name='home',
            name='home_h1',
            field=models.CharField(help_text='До 100 символов', max_length=100, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='home',
            name='meta_description',
            field=models.CharField(blank=True, help_text='До 300 символов', max_length=300, null=True, verbose_name='Метатэг description'),
        ),
        migrations.AlterField(
            model_name='home',
            name='meta_keywords',
            field=models.CharField(blank=True, help_text='До 150 символов', max_length=150, null=True, verbose_name='Метатег Keywords'),
        ),
        migrations.AlterField(
            model_name='home',
            name='title',
            field=models.CharField(help_text='До 70 символов', max_length=70, verbose_name='Метатэг Title'),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(db_index=True, help_text='До 100 символов', max_length=100, unique=True, verbose_name='Заголовок'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_annotation',
            field=models.CharField(blank=True, help_text='До 150 символов', max_length=150, null=True, verbose_name='Аннотация - выводится в карточке продукта'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(db_index=True, help_text='До 90 символов', max_length=90, unique=True, verbose_name='Наименование'),
        ),
        migrations.AlterField(
            model_name='version',
            name='description',
            field=models.CharField(help_text='До 250 символов', max_length=250, verbose_name='Улучшения версии'),
        ),
        migrations.AlterField(
            model_name='version',
            name='status',
            field=models.CharField(choices=[('активно', 'ДА'), ('неактивно', 'НЕТ')], default='неактивно', max_length=10, verbose_name='Активная?'),
        ),
        migrations.AlterField(
            model_name='version',
            name='value',
            field=models.CharField(max_length=10, verbose_name='Номер'),
        ),
    ]
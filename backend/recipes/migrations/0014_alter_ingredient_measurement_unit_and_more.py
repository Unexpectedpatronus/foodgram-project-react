# Generated by Django 4.1.10 on 2023-07-15 19:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_alter_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(1, message='Должен быть минимум 1 символ!')], verbose_name='Единица измерения ингредиента'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(1, message='Должен быть минимум 1 символ!')], verbose_name='Название ингредиента'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='name',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.MinLengthValidator(1, message='Должен быть минимум 1 символ!')], verbose_name='Название рецепта'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True, validators=[django.core.validators.MinLengthValidator(1, message='Должен быть минимум 1 символ!')], verbose_name='Имя тега'),
        ),
    ]

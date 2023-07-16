# Generated by Django 4.1.10 on 2023-07-16 19:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='ingredientamountinrecipe',
            name='unique_IngredientToRecipe',
        ),
        migrations.AlterField(
            model_name='favourite',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='recipes.recipe', verbose_name='Рецепт'),
        ),
        migrations.AlterField(
            model_name='favourite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Имя тега'),
        ),
        migrations.AddConstraint(
            model_name='ingredientamountinrecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_IngredientAmountInRecipe'),
        ),
    ]

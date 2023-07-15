from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import (MaxValueValidator, MinLengthValidator,
                                    MinValueValidator)
from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Length

MAXLENGTH: int = 15
models.CharField.register_lookup(Length)
User = get_user_model()


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        'Имя тега',
        max_length=200,
        unique=True,
        validators=[
            MinLengthValidator(1, message='Должен быть минимум 1 символ!')
        ]
    )
    COLOR_PALETTE = [
        ("#E26C2D", "Завтрак",),
        ("#008000", "Обед",),
        ("#7366BD", "Ужин",),
    ]
    color = ColorField(
        format="hexa",
        samples=COLOR_PALETTE,
        unique=True
    )

    slug = models.SlugField(
        'Слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return self.name[:MAXLENGTH]


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        'Название ингредиента',
        max_length=200,
        validators=[
            MinLengthValidator(1, message='Должен быть минимум 1 символ!')
        ]
    )
    measurement_unit = models.CharField(
        'Единица измерения ингредиента',
        max_length=20,
        validators=[
            MinLengthValidator(1, message='Должен быть минимум 1 символ!')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit}).'


class Recipe(models.Model):
    """Модель рецепта."""
    name = models.CharField(
        'Название рецепта',
        max_length=200,
        unique=True,
        validators=[
            MinLengthValidator(1, message='Должен быть минимум 1 символ!')
        ]
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipes/',
        null=True,
        default=None
    )
    text = models.TextField(
        'Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег',
        related_name='recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления, мин',
        validators=(
            MinValueValidator(1, message='Минимальное значение = 1!'),
            MaxValueValidator(32767, message='Максимальное значение = 32767!')
        )
    )
    date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-date',)
        constraints = [
            UniqueConstraint(
                fields=('name', 'author'),
                name='unique_name_author'
            )
        ]

    def __str__(self):
        return f'{self.author.username}, автор {self.name[:MAXLENGTH]}'


class RecipeIngredient(models.Model):
    """Модель связи рецепта и ингредиентов."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipeingredient'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        related_name='recipeingredient'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(
            MinValueValidator(1, message='Минимальное значение = 1!'),
            MaxValueValidator(32767, message='Максимальное значение = 32767!')
        )
    )

    class Meta:
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'
        ordering = ('recipe',)
        constraints = [
            UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.ingredient} ({self.amount}) in {self.recipe}'


class Favourite(models.Model):
    """Модель избранного."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favourites'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Понравившиеся рецепты',
        on_delete=models.CASCADE,
        related_name='favourites'
    )
    date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favourite'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в избранное'


class ShoppingCart(models.Model):
    """Модель списка покупок."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shopping_cart'
    )
    date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart')
        ]

    def __str__(self):
        return f'Добавлено в корзину {self.recipe}'

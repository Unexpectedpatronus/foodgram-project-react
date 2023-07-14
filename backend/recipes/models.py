from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User

MAXLENGTH: int = 15


class Tag(models.Model):
    """Модель тегов."""

    name = models.CharField(
        'Имя тега',
        max_length=200,
        unique=True
    )

    color = ColorField(
        format="hexa",
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
        max_length=200
    )
    measurement_unit = models.CharField(
        'Единица измерения ингредиента',
        max_length=20
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.measurement_unit}).'


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200
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
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-date',)

    def __str__(self):
        return f'{self.author.email}, {self.name[:MAXLENGTH]}'


class RecipeIngredient(models.Model):
    """Модель ингредиентов для рецепта."""

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
        constraints = (
            UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_recipe_ingredient'
            ),
        )

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

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favourite'
            ),
        )

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

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = (
            UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart'),
        )

    def __str__(self):
        return f'Добавлено в корзину {self.recipe}'

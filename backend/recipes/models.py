from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from foodgram.global_constants import (INGREDIENT_NAME_LENGTH, MAXLENGTH,
                                       MEASUREMENT_UNIT_LENGTH,
                                       RECIPE_NAME_LENGTH, SLUG_LENGTH,
                                       TAG_NAME_LENGTH)
from users.models import User


class Tag(models.Model):
    """Модель тэгов."""

    name = models.CharField(
        'Имя тега',
        help_text='Название тэга',
        max_length=TAG_NAME_LENGTH,
        unique=True
    )
    COLOR_PALETTE = [
        ("#E26C2D", "Завтрак",),
        ("#008000", "Обед",),
        ("#7366BD", "Ужин",),
    ]
    color = ColorField(
        format="hex",
        samples=COLOR_PALETTE,
        unique=True,
    )
    slug = models.SlugField(
        'Слаг',
        help_text='Имя для URL',
        max_length=SLUG_LENGTH,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['-id']

    def __str__(self):
        return self.name[:MAXLENGTH]

    def clean(self):
        self.color = self.color.lower().strip()
        self.name = self.name.lower().strip()
        self.slug = self.slug.lower().strip()
        super().clean()


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        'Название ингредиента',
        help_text='Название ингредиента',
        max_length=INGREDIENT_NAME_LENGTH
    )
    measurement_unit = models.CharField(
        'Единица измерения ингредиента',
        help_text='Единица измерения количества ингредиентов',
        max_length=MEASUREMENT_UNIT_LENGTH,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_name_measurement_unit'
            )
        ]

    def __str__(self):
        return (f'{self.name[:MAXLENGTH]} '
                f'({self.measurement_unit[:MAXLENGTH]}).')

    def clean(self):
        self.name = self.name.lower()
        self.measurement_unit = self.measurement_unit.lower()
        super().clean()


class Recipe(models.Model):
    """Модель рецепта."""

    name = models.CharField(
        'Название рецепта',
        max_length=RECIPE_NAME_LENGTH,
        unique=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        help_text='Автор публикации рецепта',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    image = models.ImageField(
        'Фото рецепта',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        help_text='Ингредиенты для приготовления по рецепту',
        through='IngredientInRecipesAmount',
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
        help_text='Тэги по рецепту',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления, мин',
        help_text='Время приготовления блюда',
        validators=(
            MinValueValidator(1, message='Минимальное значение = 1!'),
            MaxValueValidator(32767, message='Максимальное значение = 32767!')
        )
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_name_author'
            )
        ]

    def __str__(self):
        return f'{self.author}, автор {self.name}'

    def clean(self):
        self.name = self.name.capitalize()
        existing_recipe = Recipe.objects.filter(
            name=self.name
        ).exclude(id=self.id).first()
        if existing_recipe:
            raise ValidationError(
                {'name': 'Рецепт с таким названием уже существует!'}
            )
        super().clean()


class IngredientInRecipesAmount(models.Model):
    """Модель связи рецепта и ингредиентов."""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='recipe',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиент',
    )

    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        help_text='Необходимое количество данного ингредиента',
        validators=(
            MinValueValidator(1, message='Минимальное значение = 1!'),
            MaxValueValidator(32767, message='Максимальное значение = 32767!')
        )
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ('recipe',)
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient',
            )
        ]

    def __str__(self):
        return f'{self.ingredient} ({self.amount}) в {self.recipe}'


class FavoriteReceipe(models.Model):
    """Модель избранного."""

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite_user',
    )

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Понравившиеся рецепты',
        on_delete=models.CASCADE,
        related_name='favorite_recipes',
    )
    date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Рецепты в избранном'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='favorite_recipe',
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
        related_name='shopping_user',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепты',
        on_delete=models.CASCADE,
        related_name='shopping_recipes',
    )

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_shopping_cart',
            )
        ]

    def __str__(self):
        return f'Добавлено в корзину {self.recipe}'

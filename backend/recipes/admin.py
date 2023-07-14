from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from recipes.models import (Favourite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)

EMPTY_STRING: str = '-пусто-'


class RequiredInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        if not any(form.cleaned_data for form in self.forms):
            raise forms.ValidationError('Должен быть хотя бы 1 ингредиент.')


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    formset = RequiredInlineFormSet


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'author',
        'get_ingredients',
        'get_tags',
        'count_favourites',
    )

    inlines = [RecipeIngredientInline]

    search_fields = ('author__username', 'name', 'tags__name',)

    list_filter = ('author', 'name', 'tags')

    def get_ingredients(self, object):
        return ',\n'.join(
            ingredient.name for ingredient in object.ingredients.all()
        )

    get_ingredients.short_description = 'Ингредиенты'

    def get_tags(self, object):
        return '\n'.join(tag.name for tag in object.tags.all())

    get_tags.short_description = 'Теги'

    def count_favourites(self, object):
        return object.favourites.count()

    count_favourites.short_description = 'Раз в избранном'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name', 'color')
    empty_value_display = EMPTY_STRING


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'get_ingredients',)

    def get_ingredients(self, object):
        return ',\n'.join(
            ingredient.name for ingredient in object.recipe.ingredients.all()
        )

    get_ingredients.short_description = 'Ингредиенты'


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount',)

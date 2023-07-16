from django.db.models.aggregates import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from api.filters import NameSearchFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAdminOrAuthorOrReadOnly
from api.serializers import (FollowSerializer, IngredientSerializer,
                             MyUserSerializer, RecipeCreateSerializer,
                             RecipeSerializer, RecipeShowSerializer,
                             TagSerializer, UserFollowSerializer)
from recipes.models import (Favourite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from users.models import Follow, User


class MyUserViewSet(UserViewSet):
    """Вьюсет для пользователей и подписок."""

    queryset = User.objects.all()
    serializer_class = MyUserSerializer
    pagination_class = CustomPagination

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(author__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = UserFollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True,
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated,))
    def subscribe(self, request, **kwargs):
        user = request.user
        author_id = self.kwargs.get('id')
        author = get_object_or_404(User, id=author_id)

        if request.method == 'POST':
            serializer = FollowSerializer(
                data={
                    'user': user.id,
                    'author': author.id,
                },
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(
                user=user,
                author=author
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        subscription = get_object_or_404(
            Follow,
            user=request.user,
            author=author
        )

        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    filter_backends = (NameSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    def add_recipe(self, model, user, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        serializer = RecipeShowSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(Favourite, request.user, pk)
        return self.delete_recipe(Favourite, request.user, pk)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request.user, pk)
        return self.delete_recipe(ShoppingCart, request.user, pk)

    @action(
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = RecipeIngredient.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount_sum=Sum('amount'))

        today = timezone.now()
        shopping_card_list = (
            f'Список покупок для: {user.get_full_name()}\n\n'
            f'Дата: {today:%d.%m.%Y}\n'
        )
        shopping_card_list += '\n'.join([
            f'+ {ingredient["ingredient__name"]} '
            f'({ingredient["ingredient__measurement_unit"]})'
            f' - {ingredient["amount_sum"]}'
            for ingredient in ingredients
        ])
        shopping_card_list += f'\n\nFoodgram ({today:%Y})'

        filename = f'{user.username}_shopping_card_list.txt'
        response = HttpResponse(shopping_card_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'

        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None

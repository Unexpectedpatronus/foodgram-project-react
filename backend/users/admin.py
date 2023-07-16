from django.contrib import admin

from .models import Follow, User

EMPTY_VALUE = '-пусто-'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Отображение и фильтр полей User в админке."""

    list_display = ('id', 'username', 'first_name', 'last_name', 'email',)
    search_fields = ('username', 'email',)
    list_filter = ('first_name', 'email',)
    list_display_links = ('username',)
    empty_value = EMPTY_VALUE


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Отображение, фильтр, поиск полей Follow в админке."""

    list_display = ('user', 'author')
    list_filter = ('user', 'author')
    search_fields = ('user', 'author')
    empty_value = EMPTY_VALUE

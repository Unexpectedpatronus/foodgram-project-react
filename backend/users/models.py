from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models

from foodgram.global_constants import (EMAIL_LENGTH, FIRST_NAME_LENGTH,
                                       LAST_NAME_LENGTH, MAXLENGTH,
                                       PASSWORD_LENGTH, USERNAME_LENGTH)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name',)

    email = models.EmailField(
        'Почта',
        max_length=EMAIL_LENGTH,
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        validators=(UnicodeUsernameValidator,),
        max_length=USERNAME_LENGTH,
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=FIRST_NAME_LENGTH,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=LAST_NAME_LENGTH,
        blank=True,
    )
    password = models.CharField(
        'Пароль',
        max_length=PASSWORD_LENGTH,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('pk',)
        constraints = [
            models.UniqueConstraint(
                fields=('email', 'username'),
                name='unique_auth'
            )
        ]

    def __str__(self):
        return self.username[:MAXLENGTH]


class Follow(models.Model):
    """Модель подписок."""

    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписчик'
        verbose_name_plural = 'Подписчики'
        ordering = ('-pk',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription'
            )
        ]

    def clean(self):
        if self.user == self.author:
            raise ValidationError('Нельзя подписаться на самого себя!')
        super().clean()

    def __str__(self):
        return f'{self.user} подписан на {self.author}'

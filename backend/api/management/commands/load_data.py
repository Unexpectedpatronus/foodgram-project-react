import json

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    '''Выполнить команду python manage.py load_data.'''

    help = 'Импорт данных из файла ingredients.json'

    def handle(self, *args, **kwargs):
        with open(f'{settings.BASE_DIR}/data/ingredients.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        for row in data:
            Ingredient.objects.get_or_create(**row)

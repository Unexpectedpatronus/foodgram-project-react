import datetime
import json

from django.conf import settings
from django.core.management import BaseCommand

from recipes.models import Ingredient

FILE = f'{settings.BASE_DIR}/data/ingredients.json'


def import_json_data():
    """ Обработка файла json. """

    with open(FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for row in data:
            Ingredient.objects.get_or_create(**row)


class Command(BaseCommand):
    """Выполнить команду python manage.py load_data."""

    help = 'Импорт данных из файла ingredients.json'

    def handle(self, *args, **options):
        start_time = datetime.datetime.now()
        try:
            import_json_data()
        except Exception as error:
            self.stdout.write(
                self.style.WARNING(f'Сбой в работе импорта: {error}.')
            )
        else:
            self.stdout.write(self.style.SUCCESS(
                f'Загрузка данных завершена за '
                f' {(datetime.datetime.now() - start_time).total_seconds()} '
                f'сек.')
            )

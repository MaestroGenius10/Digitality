# myapp/management/commands/add_categories.py

from django.core.management.base import BaseCommand
from myapp.models import Category

class Command(BaseCommand):
    help = 'Add initial categories to the database'

    def handle(self, *args, **kwargs):
        categories = [
            'Смартфоны',
            'Смарт-часы',
            'Наушники',
            'Телевизоры',
            'Ноутбуки',
            'ПК'
        ]
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
        self.stdout.write(self.style.SUCCESS('Все категории успешно добавлены'))

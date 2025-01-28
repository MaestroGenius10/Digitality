from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connection, transaction

class Command(BaseCommand):
    help = 'Очистить все таблицы в базе данных'

    def handle(self, *args, **kwargs):
        self.clear_database()
        self.stdout.write(self.style.SUCCESS('Все таблицы успешно очищены!'))

    def clear_database(self):
        """Очищает все таблицы в базе данных."""
        all_models = apps.get_models()
        table_names = [model._meta.db_table for model in all_models]

        try:
            # Отключаем транзакции для очистки таблиц
            with transaction.atomic():
                cursor = connection.cursor()
                for table in table_names:
                    cursor.execute(f"TRUNCATE TABLE {table} CASCADE;")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при очистке базы данных: {e}"))

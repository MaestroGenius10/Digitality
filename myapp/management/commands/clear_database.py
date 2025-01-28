import os
import django
from django.apps import apps
from django.db import connection, transaction

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

def clear_database():
    """Очищает все таблицы в базе данных."""
    with connection.cursor() as cursor:
        all_models = apps.get_models()
        table_names = [model._meta.db_table for model in all_models]

        try:
            cursor.execute("TRUNCATE TABLE {} CASCADE;".format(", ".join(table_names)))
            print("Все таблицы успешно очищены!")
        except Exception as e:
            print(f"Ошибка при очистке базы данных: {e}")

if __name__ == "__main__":
    clear_database()

# Проект Digitality

Это проект, разработанный для создания электронной торговой платформы для пользователей. В этом документе описаны шаги для настройки проекта и его запуска на вашем компьютере.

## Шаги для настройки и запуска проекта

### 1. Клонируйте репозиторий

Чтобы начать работу с проектом, сначала клонируйте репозиторий на ваш компьютер:

git clone https://github.com/MaestroGenius10/Digitality

далее переходим в нужную папку
cd Digitality

после вводим следующие команды:
python -m venv venv
.\venv\Scripts\activate (если работаем в git bash, то команда source venv/Scripts/activate)
устанавливаем зависимости
pip install -r requirements.txt

после открываем проект в PyCharm
python manage.py clear_database (для очистки базы данных)
python manage.py add_categories (для добавления предопределённых категорий товаров)
python manage.py runserver (для запуска сервера)





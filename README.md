# Проект Digitality

Это проект, разработанный для создания электронной торговой платформы для пользователей. В этом документе описаны шаги для настройки проекта и его запуска на вашем компьютере.

## Шаги для настройки и запуска проекта
Чтобы начать работу с проектом, сначала клонируйте репозиторий на ваш компьютер:

- **git clone https://github.com/MaestroGenius10/Digitality**

далее переходим в нужную папку
- **cd Digitality**

после вводим следующие команды:
- **python -m venv venv**
- **.\venv\Scripts\activate** (если работаем в git bash, то команда source venv/Scripts/activate)
устанавливаем зависимости
pip install -r requirements.txt

после открываем проект в PyCharm
- **python manage.py makemigrations**
- **python manage.py migrate**
- **python manage.py clear_database** (для очистки базы данных
- **python manage.py add_categories** (для добавления предопределённых категорий товаров)
- **python manage.py runserver** (для запуска сервера)

## Основные модели проекта

- **User**: Модель представляет пользователя системы. Хранит данные о пользователе, включая имя, email, пароль, фото профиля и дату рождения.
  
- **Category**: Модель представляет категорию товаров. Используется для группировки товаров в различные категории.

- **Product**: Модель представляет товар, доступный для покупки. Хранит информацию о товаре, такую как имя, описание, цена, категория и изображение.

- **Cart**: Модель представляет корзину покупок для пользователя. Каждый пользователь имеет свою корзину, в которой могут находиться товары.

- **CartItem**: Модель представляет товар в корзине пользователя. Хранит связь с товаром и количество, которое добавлено в корзину.

- **Order**: Модель представляет заказ пользователя. Хранит информацию о заказе, включая пользователя, общую стоимость, статус и дату создания.

- **OrderItem**: Модель представляет товар в заказе. Содержит информацию о заказанном товаре, количестве и цене на момент покупки.

- **PaymentCard**: Модель представляет платежную карту пользователя. Хранит информацию о карте, включая номер, имя владельца, дату истечения срока действия и CVV.


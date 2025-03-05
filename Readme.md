API Payment System

Описание

Простая система оплаты с использованием Django и Stripe API.

Требования

Python 3.10+

Django 4+

Stripe API

Установленный pip и virtualenv

Установка и запуск

1. Клонирование репозитория

git clone <repo_url>
cd <project_folder>

2. Создание виртуального окружения и установка зависимостей

python -m venv venv
source venv/bin/activate  # для macOS/Linux
venv\Scripts\activate  # для Windows
pip install -r requirements.txt

3. Настройка переменных окружения

Создайте файл .env в корневой папке проекта и добавьте туда ключи:

DJANGO_SECRET_KEY=<your_django_secret_key>
STRIPE_SECRET_KEY=<your_stripe_secret_key>
STRIPE_PUBLIC_KEY=<your_stripe_public_key>
STRIPE_WEBHOOK_SECRET=<your_stripe_webhook_secret>

4. Применение миграций и запуск сервера

python manage.py migrate
python manage.py runserver

Сервер запустится на http://127.0.0.1:8000/

Работа с платежами

Покупка товара

Для покупки отдельного товара отправьте POST-запрос на:

/buy/{item_id}/

Создание заказа

Для создания заказа отправьте POST-запрос с массивом товаров:

/create-order/

Оплата заказа

Оплатить заказ можно по пути:

/buy-order/{order_id}/

Webhook

Stripe отправляет данные о платежах на endpoint:

/stripe-webhook/

Не забудьте настроить его в вашем Stripe-аккаунте.
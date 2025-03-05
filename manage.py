import os
import sys
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application  # Импортируем WSGI-приложение

# Загружаем переменные окружения из .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# Настройка для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

# Точка входа для Vercel
application = get_wsgi_application()  # Применяем переменную `application`


def main():
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError("Не удалось импортировать Django. Убедись, что он установлен.")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

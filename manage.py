import os
import sys
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        raise ImportError("Не удалось импортировать Django. Убедись, что он установлен.")

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

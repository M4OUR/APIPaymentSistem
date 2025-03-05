import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

# Точка входа для Vercel
app = get_wsgi_application()  # Используем переменную app, а не application

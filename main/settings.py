import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()

# Основные настройки Django
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
DEBUG = True
ALLOWED_HOSTS = ['*']

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'payments',
    'main',
    'csp',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'csp.middleware.CSPMiddleware',
]

# Конфигурация URL
ROOT_URLCONF = 'main.urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI-приложение
WSGI_APPLICATION = 'main.wsgi.application'

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'APIPayments',
        'USER': 'postgres',
        'PASSWORD': 'qwer2233',
        'HOST': 'db.ieejsaznddgcesrwwwvm.supabase.co',
        'PORT': '5432',  
    }
}

# Настройки Content Security Policy для Stripe
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", 'https://js.stripe.com', "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", 'data:', 'https://*')
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_CONNECT_SRC = (
    "'self'",
    "https://m.stripe.network",
    "wss://m.stripe.network",
    "https://m.stripe.com",
    "https://api.stripe.com",
    "https://r.stripe.com",
    "https://checkout.stripe.com",
    "https://js.stripe.com",
)
CSP_FRAME_SRC = (
    "'self'",
    "https://js.stripe.com",
    "https://checkout.stripe.com",
    "https://m.stripe.network",
)

DOMAIN = "http://127.0.0.1:8000"

# Настройки статики
STATIC_URL = '/static/'

# Разрешенные источники для CSRF
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']

# Автогенерация поля ID
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ключи Stripe
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY")

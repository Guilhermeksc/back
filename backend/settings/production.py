# settings/production.py

from .base import *

CURRENT_ENVIRONMENT = "Production"

BASE_URL = "https://www.licitacao360.com"

SECRET_KEY = "8v#+9z%j6_(&o94so)pvr0x^v!5a(c2dy$73+0#_5!1is&)(mr"

DEBUG = True

ALLOWED_HOSTS='licitacao360.com,www.licitacao360.com'

from corsheaders.defaults import default_headers

CORS_ALLOWED_ORIGINS = [
    "https://www.licitacao360.com",
    "https://licitacao360.com",
]

CORS_ALLOW_HEADERS = list(default_headers) + [
    'X-CSRFToken',
]

CORS_ALLOW_CREDENTIALS = True  # Permitir credenciais

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME", "licitacao360"),
        'USER': os.getenv("DB_USER", "postgres"),
        'PASSWORD': os.getenv("DB_PASSWORD", "@Licitacao360.1000"),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

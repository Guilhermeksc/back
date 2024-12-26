# settings/development.py

from .base import *

CURRENT_ENVIRONMENT = "Development"

BASE_URL = "http://127.0.0.1:8000"

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
]

INSTALLED_APPS += ['debug_toolbar']


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Deve estar no topo
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Logo após CommonMiddleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: not request.is_ajax() and not request.path.startswith('/api/')
}

INTERNAL_IPS = [
    "127.0.0.1",
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'licitacao360',
        'USER': 'postgres',
        'PASSWORD': '@Licitacao360.1000',
        'HOST': 'localhost',  # ou o IP do servidor PostgreSQL
        'PORT': '5432',       # Porta padrão do PostgreSQL
    }
}
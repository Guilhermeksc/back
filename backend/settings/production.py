# settings/production.py

from .base import *

CURRENT_ENVIRONMENT = "Production"

BASE_URL = "https://www.licitacao360.com"

SECRET_KEY = "8v#+9z%j6_(&o94so)pvr0x^v!5a(c2dy$73+0#_5!1is&)(mr"

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

CORS_ALLOWED_ORIGINS = [
    "https://www.licitacao360.com",
]

CORS_ALLOW_CREDENTIALS = True  # Permitir credenciais


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

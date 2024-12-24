"""
Django settings for backend project.
"""

from datetime import timedelta
from pathlib import Path
import os

# Determinar o ambiente (produção ou desenvolvimento)
ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

# URL base para o frontend
if ENVIRONMENT == 'production':
    FRONTEND_BASE_URL = "https://www.licitacao360.com"
else:
    FRONTEND_BASE_URL = "http://localhost:4200"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

try:
    from .email_settings import *
except ImportError:
    print("Arquivo de configurações de e-mail não encontrado.")
    
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-le-fmd9xx5e@o0s3c5x)6a2!8v7o5cj!qsrjzkr$g%stt5#6do'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    'licitacao360.com', 
    'www.licitacao360.com', 
    'ayabioarquitetura.com', 
    'www.ayabioarquitetura.com'
]
# Application definition

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
    'corsheaders.middleware.CorsMiddleware',  # Deve estar no topo
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',       
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = False

# CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    'https://www.licitacao360.com',
    'https://licitacao360.com',
]
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-requested-with",
    "accept",
    "origin",
    "x-csrftoken",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', 
    ],
}

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Use um diretório específico para templates Django
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

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

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    'api.authentication.ActiveUserBackend',
    'django.contrib.auth.backends.ModelBackend',
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# URL e diretório raiz para arquivos estáticos
STATIC_URL = '/static/' 
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# Diretórios adicionais de arquivos estáticos (se necessário)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração para servir os arquivos de build do Angular
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'static')]


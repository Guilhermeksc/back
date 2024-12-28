## backend/wsgi.py

import os
from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.development')

application = get_wsgi_application()

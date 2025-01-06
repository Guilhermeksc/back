## backend/asgi.py

import os
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do arquivo .env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()

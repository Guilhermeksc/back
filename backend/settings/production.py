# settings/production.py

from .base import *
from corsheaders.defaults import default_headers


DEBUG = False

# BASE_URL = "https://licitacao360.com"

# ALLOWED_HOSTS = ['licitacao360.com', 'www.licitacao360.com']

# Segurança em produção
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# CORS_ALLOWED_ORIGINS = [
#     "https://www.licitacao360.com",
#     "https://licitacao360.com",
# ]

# CORS_ALLOW_HEADERS = list(default_headers) + [
#     'X-CSRFToken',
# ]

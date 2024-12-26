import os

ENVIRONMENT = os.getenv("DJANGO_ENV", "development")  # Padrão: desenvolvimento

if ENVIRONMENT == "production":
    from .production import *
    print("Using Production Settings")
elif ENVIRONMENT == "development":
    from .development import *
    print("Using Development Settings")
else:
    raise ValueError(f"Ambiente desconhecido: {ENVIRONMENT}")
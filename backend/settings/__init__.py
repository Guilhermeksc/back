import os

# Obter o ambiente do Django (padrão: development)
ENVIRONMENT = os.getenv("DJANGO_ENV", "development").lower()

if ENVIRONMENT == "production":
    from .production import *  # Importa as configurações de produção
    print("Usando as configurações de PRODUÇÃO.")
elif ENVIRONMENT == "development":
    from .development import *  # Importa as configurações de desenvolvimento
    print("Usando as configurações de DESENVOLVIMENTO.")
else:
    raise ValueError(f"Ambiente desconhecido: {ENVIRONMENT}. Configure DJANGO_ENV como 'development' ou 'production'.")

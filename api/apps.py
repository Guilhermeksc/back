from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        import api.signals  # Certifique-se de que 'api.signals' existe
        # Não manipule diretamente User ou outros modelos aqui

from django.apps import AppConfig


class AppContratosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_contratos'

    def ready(self):
        import app_contratos.signals

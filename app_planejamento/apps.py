from django.apps import AppConfig

class AppPlanejamentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_planejamento'

    def ready(self):
        import api.signals

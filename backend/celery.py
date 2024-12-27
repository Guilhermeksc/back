from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo de configuração padrão do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.development')

app = Celery('backend')

# Lê as configurações do Django para Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente as tarefas de todos os aplicativos instalados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

## backend/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define o módulo de configuração padrão do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Configuração Celery
app.conf.update(
    broker_connection_retry_on_startup=True,  # Configuração para retry no startup
    broker_url='redis://localhost:6379/0',    # URL do Redis
    result_backend='redis://localhost:6379/0',  # Backend para resultados
    task_track_started=True,                 # Monitora o início das tarefas
    task_time_limit=300                      # Tempo limite das tarefas (ajuste conforme necessário)
)

# Lê as configurações do Django para Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente as tarefas de todos os aplicativos instalados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

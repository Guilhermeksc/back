from __future__ import absolute_import, unicode_literals

# Isso garante que o Celery é carregado ao iniciar o Django
from .celery import app as celery_app

__all__ = ('celery_app',)

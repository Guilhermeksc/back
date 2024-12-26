# api/signals.py

from django.db.models.signals import post_save
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.db import connection

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Cria automaticamente um perfil para novos usuários.
    """
    if created:
        try:
            Profile.objects.create(user=instance)
            print(f"Perfil criado para o usuário: {instance.username}")
        except Exception as e:
            print(f"Erro ao criar perfil para o usuário {instance.username}: {e}")

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from api.models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Só cria o Profile se ele ainda não existir
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Salva o Profile existente
    if hasattr(instance, 'profile'):
        instance.profile.save()
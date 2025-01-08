from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    validation_token = models.CharField(max_length=64, blank=True, null=True)
    reset_password_token = models.CharField(max_length=64, blank=True, null=True)
    unidade_compra = models.CharField(max_length=20, blank=True, null=True) 

    def __str__(self):
        return f"Perfil de {self.user.email}"
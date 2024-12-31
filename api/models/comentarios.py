from django.db import models

class Comentario(models.Model):
    numero = models.CharField(max_length=50)
    uasg = models.CharField(max_length=50)
    comentario = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)  # Define a data de criação
    atualizado_em = models.DateTimeField(auto_now=True)  # Atualiza automaticamente na modificação

    def __str__(self):
        return f"{self.numero} - {self.uasg}"

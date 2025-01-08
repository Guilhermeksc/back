from rest_framework import serializers
from .models import Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'numero', 'unidade_compra', 'comentario', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']  # Campos somente leitura

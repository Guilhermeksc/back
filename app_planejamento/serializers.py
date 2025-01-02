# app_planejamento/serializers.py

from rest_framework import serializers
from .models import ControleProcessos

class ControleProcessosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControleProcessos
        fields = [
            'id_processo', 'etapa', 'situacao', 'material_servico', 
            'nup', 'objeto', 'uasg', 'valor_total'
        ]
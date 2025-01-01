from rest_framework import serializers
from .models import Comentario, ControleProcessos


class ControleProcessosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ControleProcessos
        fields = '__all__'

    def validate(self, data):
        required_fields = ['id_processo', 'objeto', 'sigla_om']
        errors = {}
        for field in required_fields:
            if not data.get(field):
                errors[field] = [f"O campo '{field}' é obrigatório."]
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def validate_id_processo(self, value):
        if not value:
            raise serializers.ValidationError("O campo 'id_processo' é obrigatório.")
        if len(value) > 100:
            raise serializers.ValidationError("O campo 'id_processo' não pode exceder 100 caracteres.")
        return value

    def validate_uasg(self, value):
        if len(value) != 5:
            raise serializers.ValidationError("O campo 'uasg' deve ter exatamente 5 caracteres.")
        return value
    
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = ['id', 'numero', 'uasg', 'comentario', 'criado_em', 'atualizado_em']
        read_only_fields = ['criado_em', 'atualizado_em']  # Campos somente leitura

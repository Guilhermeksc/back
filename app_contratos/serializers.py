# app_planejamento/serializers.py

from rest_framework import serializers
from .models import controlecomprasnetcontratos, Comentario

class controlecomprasnetcontratosSerializer(serializers.ModelSerializer):
    class Meta:
        model = controlecomprasnetcontratos
        fields = "__all__"

    def validate_codigo_orgao(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("O código do órgão deve conter apenas números.")
        return value
        
        
class ContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = controlecomprasnetcontratos
        fields = "__all__"

    def validate_codigo_orgao(self, value):
        if value and not value.isdigit():
            raise serializers.ValidationError("O código do órgão deve conter apenas números.")
        return value
    
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

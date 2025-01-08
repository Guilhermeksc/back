# app_planejamento/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import ControleProcessos
from .serializers import ControleProcessosSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class ControleProcessosViewSet(viewsets.ModelViewSet):
    queryset = ControleProcessos.objects.all()
    serializer_class = ControleProcessosSerializer
    permission_classes = [IsAuthenticated]  # Exigir autenticação

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:  # Confirmação de autenticação
            return ControleProcessos.objects.none()  # Retorna vazio para usuários não autenticados
        unidade_compra = user.profile.unidade_compra  # Obter a UASG do perfil
        return ControleProcessos.objects.filter(unidade_compra=unidade_compra)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        print('Dados recebidos no backend:', request.data)  # Log dos dados recebidos
        return Response(serializer.data, status=status.HTTP_201_CREATED)
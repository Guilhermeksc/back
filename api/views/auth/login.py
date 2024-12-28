# src/api/views/auth.py

from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import logging

logger = logging.getLogger(__name__)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Adicione logs para depuração
        print("Dados recebidos no POST:", request.data)

        if not username or not password:
            return Response({'detail': 'Username e senha são obrigatórios.'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user:
            # Gera o token JWT
            refresh = RefreshToken.for_user(user)

            # Retorna os dados necessários para o frontend
            user_data = {
                "token": str(refresh.access_token),
                "username": user.email,  # Substituído para retornar o e-mail
                "is_active": user.is_active,  # Adicionado para incluir o estado de ativação
            }

            return Response(user_data, status=200)
        
        # Retorna uma resposta caso as credenciais sejam inválidas
        return Response({'detail': 'Credenciais inválidas.'}, status=401)
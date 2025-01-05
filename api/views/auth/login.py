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

        # Log para depuração
        print("DEBUG: Dados recebidos no POST:", request.data)

        if not username or not password:
            return Response({'detail': 'Username e senha são obrigatórios.'}, status=400)

        user = authenticate(request, username=username, password=password)

        if user:
            # Gera o token JWT
            refresh = RefreshToken.for_user(user)

            # Obtém o campo UASG de forma opcional
            uasg = getattr(user.profile, 'uasg', None)  # Garante que o campo existe
            print(f"DEBUG: UASG para o usuário {user.username}: {uasg}")  # Log do UASG

            # Cria a resposta com os dados do usuário
            user_data = {
                "token": str(refresh.access_token),
                "username": user.email,  # Retorna o e-mail como username
                "is_active": user.is_active,  # Adicionado para incluir o estado de ativação
            }

            # Adiciona o UASG à resposta apenas se não for None
            if uasg:
                user_data["uasg"] = uasg

            return Response(user_data, status=200)

        # Retorna uma resposta caso as credenciais sejam inválidas
        return Response({'detail': 'Credenciais inválidas.'}, status=401)

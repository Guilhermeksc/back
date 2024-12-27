# src/api/views/auth.py

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.management.task import send_validation_email
from rest_framework import status
import time
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        start_time = time.time()
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        logger.info("Recebido POST em /api/register/")
        logger.info(f"Dados recebidos: name={name}, email={email}")

        if not name or not email or not password:
            logger.warning("Dados incompletos recebidos.")
            return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            logger.warning(f"E-mail já registrado: {email}")
            return Response({"error": "Este e-mail já está registrado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=email, email=email, password=password, first_name=name, is_active=False
                )
                logger.info(f"Usuário criado: {user.email}")

                token = get_random_string(length=64)
                user.profile.validation_token = token
                user.profile.save()

                validation_url = f"{settings.BASE_URL}/api/validate-email/{token}"

                logger.info(f"Enviando e-mail de validação para {email}")
                send_validation_email.delay(email, validation_url)

            logger.info("Resposta enviada para o frontend.")
            end_time = time.time()
            print(f"Tempo total de processamento no backend: {end_time - start_time} segundos")

            return Response(
                {"message": "Usuário registrado com sucesso. Verifique seu e-mail para validar."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            logger.error(f"Erro durante o registro: {e}")
            return Response({"error": f"Erro no registro: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

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
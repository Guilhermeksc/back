# src/api/views/auth.py

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from ...serializers import CustomTokenObtainPairSerializer, RegisterSerializer
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ["post", "options"]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # URL dinâmica para ativação
            activation_url = f"{settings.BASE_URL}/api/activate/{user.id}/"
            frontend_url = f"{settings.FRONTEND_URL}/activate/{user.id}/"

            # Enviar email de confirmação
            send_mail(
                'Confirmação de Cadastro',
                f'Clique no link para ativar sua conta:\n\n{activation_url}\n\nOu acesse pelo frontend:\n\n{frontend_url}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )

            return Response(
                {'message': 'Usuário registrado com sucesso. Verifique seu email para ativar a conta.'},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateUserView(APIView):
    permission_classes = [AllowAny]  # Permitir acesso público

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            if user.is_active:
                return Response({'message': 'Usuário já está ativo.'}, status=200)
            
            user.is_active = True
            user.save()
            return Response({'message': 'Conta ativada com sucesso.'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado.'}, status=404)

# from django.conf import settings
# from rest_framework.permissions import AllowAny
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.models import User
# from django.db import transaction
# from django.utils.crypto import get_random_string
# from rest_framework import status
# import time
# import logging
# from celery import shared_task
# from django.core.mail import send_mail
# from api.models import Profile

# logger = logging.getLogger(__name__)

# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         start_time = time.time()
#         name = request.data.get('name')
#         email = request.data.get('email')
#         password = request.data.get('password')

#         logger.info("Recebido POST em /api/register/")
#         logger.info(f"Dados recebidos: name={name}, email={email}")

#         if not name or not email or not password:
#             logger.warning("Dados incompletos recebidos.")
#             return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(email=email).exists():
#             logger.warning(f"E-mail já registrado: {email}")
#             return Response({"error": "Este e-mail já está registrado."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             with transaction.atomic():
#                 user = User.objects.create_user(
#                     username=email, email=email, password=password, first_name=name, is_active=False
#                 )
#                 logger.info(f"Usuário criado: {user.email}")

#                 # Criar o perfil, se necessário
#                 if not hasattr(user, 'profile'):
#                     Profile.objects.create(user=user)
#                     logger.info("Perfil criado manualmente.")

#                 token = get_random_string(length=64)
#                 user.profile.validation_token = token
#                 user.profile.save()

#                 validation_url = f"{settings.BASE_URL}/api/validate-email/{token}"
#                 send_validation_email.delay(email, validation_url)
#         except Exception as e:
#             logger.error(f"Erro durante o registro: {e}")
#             return Response({"error": f"Erro no registro: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def generate_token(user):
#     refresh = RefreshToken.for_user(user)
#     return str(refresh.access_token)


# logger = logging.getLogger(__name__)

# @shared_task
# def send_validation_email(email, validation_url):
#     """
#     Tarefa para enviar o e-mail de validação.
#     """
#     send_mail(
#         subject="Valide seu registro",
#         message=f"Por favor, clique no link para validar sua conta: {validation_url}",
#         from_email=settings.EMAIL_HOST_USER,
#         recipient_list=[email],
#     )


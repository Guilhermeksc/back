## src/api/views/auth/forgot_password.py

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.http import JsonResponse
import json
from api.models import Profile
import logging
from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

## src/api/views/auth/forgot_password.py

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.http import JsonResponse
import json
from api.models import Profile
import logging
from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

# src/api/views/auth/forgot_password.py
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.info("Requisição recebida para recuperação de senha.")
        try:
            data = json.loads(request.body)  # Processa o corpo da requisição como JSON
            logger.info(f"Dados recebidos: {data}")
        except json.JSONDecodeError as e:
            logger.error(f"Erro ao processar JSON: {str(e)}")
            return JsonResponse({"error": "Dados inválidos."}, status=400)

        email = data.get("email")  # Obtém o campo "email"
        if not email:
            logger.error("E-mail não fornecido.")
            return JsonResponse({"error": "E-mail é obrigatório."}, status=400)

        try:
            user = User.objects.get(email=email)
            logger.info(f"Usuário encontrado: {user.email}")
        except User.DoesNotExist:
            logger.error(f"E-mail não encontrado: {email}")
            return JsonResponse({"error": "E-mail não encontrado."}, status=404)

        # Gerar token de recuperação
        token = get_random_string(length=64)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.reset_password_token = token
        profile.save()
        logger.info(f"Token gerado: {token}")

        # Construir e enviar o e-mail de recuperação com URL do front-end
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
        logger.info(f"URL de redefinição: {reset_url}")
        send_reset_password_email.delay(email, reset_url)
        logger.info(f"Tarefa de envio de e-mail enfileirada para: {email}")

        return JsonResponse(
            {"message": "E-mail de recuperação enviado com sucesso."}, status=200
        )


@shared_task
def send_reset_password_email(email, reset_url):
    logger.info(f"Iniciando envio de e-mail para {email} com URL {reset_url}")
    try:
        send_mail(
            subject="Recuperação de Senha",
            message=f"Por favor, clique no link para redefinir sua senha: {reset_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        logger.info(f"E-mail enviado com sucesso para {email}")
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {str(e)}")
        raise

@shared_task
def send_reset_password_email(email, reset_url):
    logger.info(f"Iniciando envio de e-mail para {email} com URL {reset_url}")
    try:
        send_mail(
            subject="Recuperação de Senha",
            message=f"Por favor, clique no link para redefinir sua senha: {reset_url}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
        )
        logger.info(f"E-mail enviado com sucesso para {email}")
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {str(e)}")
        raise
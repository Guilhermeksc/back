# src/api/views/auth/reset_password.py
from rest_framework.views import APIView
from django.http import JsonResponse
from api.models import Profile
import logging
from django.http import HttpResponseRedirect
from django.conf import settings


logger = logging.getLogger(__name__)

class ResetPasswordView(APIView):
    def get(self, request, token):
        logger.info(f"Token recebido: {token}")
        try:
            # Verificar a existência do token no backend
            profile = Profile.objects.get(reset_password_token=token)
            logger.info(f"Token válido para o usuário: {profile.user.email}")

            # Redirecionar para o template do Angular
            frontend_reset_url = f"{settings.FRONTEND_URL}/reset-password/{token}"
            return HttpResponseRedirect(frontend_reset_url)

        except Profile.DoesNotExist:
            logger.error(f"Token inválido ou expirado: {token}")
            return HttpResponseRedirect(f"{settings.FRONTEND_URL}/reset-password/invalid")

    def post(self, request, token):
        logger.info(f"Token recebido: {token}")
        logger.info(f"Dados recebidos no POST: {request.data}")  # Log dos dados recebidos

        data = request.data
        new_password = data.get("new_password")

        if not new_password:
            logger.error("Erro: Nova senha não fornecida.")
            return JsonResponse({"error": "Nova senha é obrigatória."}, status=400)

        try:
            profile = Profile.objects.get(reset_password_token=token)
            logger.info(f"Usuário associado ao token: {profile.user.email}")
            user = profile.user
            user.set_password(new_password)
            user.save()

            profile.reset_password_token = None
            profile.save()

            logger.info("Senha redefinida com sucesso.")
            return JsonResponse({"message": "Senha redefinida com sucesso."}, status=200)
        except Profile.DoesNotExist:
            logger.error(f"Erro: Token inválido ou expirado: {token}")
            return JsonResponse({"error": "Token inválido ou expirado."}, status=400)
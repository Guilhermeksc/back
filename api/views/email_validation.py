# api/views/email_validation.py

from django.views import View
from django.http import JsonResponse
from api.models import Profile
import logging

logger = logging.getLogger(__name__)

class ValidateEmailView(View):
    def get(self, request, token):
        logger.info(f"Token recebido: {token}")
        try:
            profile = Profile.objects.get(validation_token=token)
            logger.info(f"Perfil encontrado: {profile.user.email}")
            profile.user.is_active = True
            profile.user.save()
            profile.validation_token = None
            profile.save()
            return JsonResponse({"message": "E-mail validado com sucesso!"}, status=200)
        except Profile.DoesNotExist:
            logger.error(f"Token inválido: {token}")
            return JsonResponse({"error": "Token inválido ou expirado."}, status=400)

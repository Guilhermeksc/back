# api/profile_manager.py
import secrets
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Profile
from django.conf import settings

class ProfileManager:
    @staticmethod
    def create_profile(user: User):
        """
        Cria um perfil associado a um usuário.
        """
        profile, created = Profile.objects.get_or_create(user=user)
        return profile

    @staticmethod
    def generate_validation_token(user: User) -> str:
        """
        Gera um token de validação único para o perfil do usuário.
        """
        token = secrets.token_urlsafe(32)
        profile = ProfileManager.create_profile(user)
        profile.validation_token = token
        profile.save()
        return token

    @staticmethod
    def send_validation_email(user: User):
        """
        Envia um e-mail de validação para o usuário.
        """
        try:
            token = ProfileManager.generate_validation_token(user)
            validation_url = f"{settings.BASE_URL}/api/validate-email/{token}/"
            send_mail(
                'Valide seu endereço de e-mail',
                f'Clique no link para validar sua conta: {validation_url}',
                'no-reply@licitacao360.com',
                [user.email],
                fail_silently=False,
            )
            logger.info(f"E-mail de validação enviado para {user.email}.")
        except Exception as e:
            logger.error(f"Erro ao enviar e-mail para {user.email}: {str(e)}")
            raise


    @staticmethod
    def validate_email_token(token: str) -> dict:
        """
        Valida o token de e-mail e ativa o usuário, se válido.
        """
        try:
            profile = Profile.objects.get(validation_token=token)
            profile.user.is_active = True
            profile.user.save()
            profile.validation_token = None
            profile.save()
            logger.info(f"Token validado com sucesso para o usuário {profile.user.email}.")
            return {"success": True, "message": "E-mail validado com sucesso!"}
        except Profile.DoesNotExist:
            logger.warning(f"Token inválido ou expirado: {token}.")
            return {"success": False, "message": "Token inválido ou expirado."}

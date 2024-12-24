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
        token = ProfileManager.generate_validation_token(user)
        validation_url = f"{settings.BASE_FRONTEND_URL}/validate-email/{token}/"

        send_mail(
            'Valide seu endereço de e-mail',
            f'Clique no link para validar sua conta: {validation_url}',
            'no-reply@licitacao360.com',
            [user.email],
            fail_silently=False,
        )

    @staticmethod
    def validate_email_token(token: str) -> bool:
        """
        Valida o token de e-mail e ativa o usuário, se válido.
        """
        try:
            profile = Profile.objects.get(validation_token=token)
            profile.user.is_active = True
            profile.user.save()
            profile.validation_token = None
            profile.save()
            return True
        except Profile.DoesNotExist:
            return False

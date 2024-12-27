# api/authentication.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class ActiveUserBackend(ModelBackend):
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)  # Autentica pelo email
            if user.check_password(password):
                if user.is_active:
                    return user
                else:
                    raise ValueError("Conta ainda não ativada.")
        except User.DoesNotExist:
            return None
        except ValueError as e:
            logging.warning(f"Tentativa de login com conta inativa: {username}")
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id, is_active=True)
        except User.DoesNotExist:
            return None


    def user_can_authenticate(self, user):
        """
        Verifica se o usuário está ativo.
        """
        return user.is_active
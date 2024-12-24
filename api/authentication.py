from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class ActiveUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
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
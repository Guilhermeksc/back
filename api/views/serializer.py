from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Verifica se o usuário está ativo
        if not user.is_active:
            raise AuthenticationFailed('Conta inativa. Verifique seu e-mail para ativar sua conta.')

        return data

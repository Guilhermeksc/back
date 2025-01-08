from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Adicione claims personalizadas
        token['username'] = user.username
        token['is_active'] = user.is_active  # Adicione o status do usuário
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user
        data['username'] = user.username
        data['is_active'] = user.is_active

        # Log para depuração
        if hasattr(user, 'profile'):
            data['unidade_compra'] = user.profile.unidade_compra
            print(f"DEBUG: UASG carregado do Profile: {data['unidade_compra']}")
        else:
            data['unidade_compra'] = None
            print("DEBUG: Usuário não possui Profile associado.")

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_active=False  # Necessário para validação de email
        )
        return user

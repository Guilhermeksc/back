from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not name or not email or not password:
            return Response({"error": "Todos os campos são obrigatórios."}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "Este e-mail já está registrado."}, status=400)

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=email, email=email, password=password, first_name=name, is_active=False
                )
                token = get_random_string(length=64)  # Gere o token
                user.profile.validation_token = token  # Salve no perfil
                user.profile.save()

                # Use a BASE_URL das configurações
                validation_url = f"{settings.BASE_URL}/api/validate-email/{token}"
                
                # Adicione prints para depuração
                print(f"Token gerado: {token}")  # Exibe o token gerado no terminal
                print(f"URL de validação: {validation_url}")  # Exibe a URL gerada

                send_mail(
                    subject="Valide seu registro",
                    message=f"Por favor, clique no link para validar sua conta: {validation_url}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                )

            return Response({"message": "Usuário registrado com sucesso. Verifique seu e-mail para validar."}, status=201)

        except Exception as e:
            return Response({"error": f"Erro no registro: {str(e)}"}, status=500)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'detail': 'Username e senha são obrigatórios.'}, status=400)

        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'username': user.username, 'token': str(refresh.access_token)}, status=200)

        return Response({'detail': 'Credenciais inválidas.'}, status=401)

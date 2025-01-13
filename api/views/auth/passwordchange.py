from django.contrib.auth.views import PasswordChangeView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

import logging

logger = logging.getLogger(__name__)
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class CustomPasswordResetView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "O e-mail é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)

            # Gera o link usando FRONTEND_URL
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

            # Envia o e-mail de redefinição de senha
            send_mail(
                subject="Redefinição de Senha",
                message=f"Use o link abaixo para redefinir sua senha:\n\n{reset_url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response({"message": "E-mail de recuperação enviado com sucesso."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.forms import SetPasswordForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
@method_decorator(csrf_exempt, name='dispatch')
class CustomPasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        print("UID:", uidb64)
        print("Token:", token)
        print("Payload recebido:", request.data)

        try:
            # Decodifica o UID e obtém o usuário
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)

            # Verifica a validade do token
            if not default_token_generator.check_token(user, token):
                return Response({"error": "Token inválido ou expirado."}, status=status.HTTP_400_BAD_REQUEST)

            # Obtém as novas senhas
            new_password1 = request.data.get("new_password1")
            new_password2 = request.data.get("new_password2")

            # Valida as senhas
            if new_password1 != new_password2:
                return Response({"error": "As senhas não coincidem."}, status=status.HTTP_400_BAD_REQUEST)

            # Define a nova senha
            form = SetPasswordForm(user, {"new_password1": new_password1, "new_password2": new_password2})
            if form.is_valid():
                form.save()
                return Response({"message": "Senha redefinida com sucesso."}, status=status.HTTP_200_OK)
            else:
                print("Erros do formulário:", form.errors)
                return Response({"error": form.errors}, status=status.HTTP_400_BAD_REQUEST)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Usuário inválido."}, status=status.HTTP_400_BAD_REQUEST)

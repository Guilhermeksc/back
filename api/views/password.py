from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

class SendPasswordResetLinkView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'E-mail é obrigatório.'}, status=400)

        try:
            user = User.objects.get(email=email)
            token = get_random_string(length=32)
            user.profile.validation_token = token
            user.profile.save()

            reset_url = f"https://www.licitacao360.com/reset-password/{token}/"
            send_mail(
                'Redefinição de Senha',
                f'Clique no link para redefinir sua senha: {reset_url}',
                'no-reply@licitacao360.com',
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Um link foi enviado para o e-mail fornecido.'}, status=200)
        except User.DoesNotExist:
            return Response({'error': 'Usuário com este e-mail não encontrado.'}, status=404)


class ChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Headers recebidos:", request.headers)  # Log para depuração
        print("Usuário autenticado:", request.user)  # Verifica o usuário autenticado

        email = request.data.get('email')
        current_password = request.data.get('currentPassword')
        new_password = request.data.get('newPassword')

        if not email or not current_password or not new_password:
            return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=email, password=current_password)
        if not user:
            return Response({"error": "Senha atual incorreta."}, status=status.HTTP_401_UNAUTHORIZED)

        if current_password == new_password:
            return Response({"error": "A nova senha não pode ser igual à senha atual."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_password = request.data.get('password')
        new_password = request.data.get('newPassword')

        if not current_password or not new_password:
            return Response({"error": "Todos os campos são obrigatórios."}, status=400)

        user = request.user
        if not user.check_password(current_password):
            return Response({"error": "Senha atual incorreta."}, status=401)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Senha alterada com sucesso."}, status=200)

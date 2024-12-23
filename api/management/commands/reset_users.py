from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

class Command(BaseCommand):
    help = 'Reseta os dados de usuários e tokens'

    def handle(self, *args, **kwargs):
        # Deletar todos os usuários
        User.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Usuários deletados com sucesso.'))

        # Resetar sequência de IDs
        with connection.cursor() as cursor:
            cursor.execute("SELECT setval(pg_get_serial_sequence('auth_user', 'id'), 1, false);")
        self.stdout.write(self.style.SUCCESS('Sequência de IDs resetada com sucesso.'))

        # Deletar tokens
        try:
            OutstandingToken.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Tokens deletados com sucesso.'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Não foi possível deletar tokens: {str(e)}'))

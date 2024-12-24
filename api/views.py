from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.views.generic import TemplateView
from django.http import Http404
from django.conf import settings
import os
import logging
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import status
from django.shortcuts import render
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.views import View
from .profile_manager import ProfileManager
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

def register_user(name, email, password):
    with transaction.atomic():
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name,
            is_active=False  # Usuário inativo até validar o e-mail
        )
        ProfileManager.send_validation_email(user)

class SendPasswordResetLinkView(View):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return JsonResponse({'error': 'E-mail é obrigatório.'}, status=400)

        try:
            user = User.objects.get(email=email)
            token = get_random_string(length=32)
            user.profile.validation_token = token  # Salve o token no Profile
            user.profile.save()

            reset_url = f"http://localhost:4200/reset-password/{token}/"

            send_mail(
                'Redefinição de Senha',
                f'Clique no link para redefinir sua senha: {reset_url}',
                'no-reply@licitacao360.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Um link foi enviado para o e-mail fornecido.'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuário com este e-mail não encontrado.'}, status=404)
        
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.user.email  # Usuário autenticado
        password = request.data.get('password')
        print(f"Tentativa de login para: {email} com senha: {password}")
        new_password = request.data.get('newPassword')

        if not email or not current_password or not new_password:
            return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Autenticar o usuário com e-mail e senha atual
            user = authenticate(username=email, password=current_password)
            if user is None:
                return Response({"error": "Senha atual incorreta."}, status=status.HTTP_401_UNAUTHORIZED)

            # Atualiza para a nova senha
            user.set_password(new_password)
            user.save()
            print(f"Senha alterada para o usuário: {user.email}")

            return Response({"message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
def index(request):
    return render(request, 'index.html') 
class FrontendAppView(TemplateView):
    template_name = "index.html"  # Agora aponta diretamente para 'index.html' em 'static'

    def get(self, request, *args, **kwargs):
        # Verifica o caminho real do template
        template_path = os.path.join(settings.TEMPLATES[0]['DIRS'][0], self.template_name)
        if not os.path.exists(template_path):
            raise Http404(f"Template não encontrado: {template_path}")
        return super().get(request, *args, **kwargs)

logger = logging.getLogger(__name__)

class ValidateEmailView(View):
    def get(self, request, token):
        if ProfileManager.validate_email_token(token):
            return JsonResponse({"message": "E-mail validado com sucesso!"}, status=200)
        return JsonResponse({"error": "Token inválido ou expirado."}, status=400)

from django.db import transaction, IntegrityError

from django.conf import settings

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Obtendo os dados do POST
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        # Verificando campos obrigatórios
        if not name or not email or not password:
            return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        # Verificando se o e-mail já está registrado
        if User.objects.filter(email=email).exists():
            return Response({"error": "Este e-mail já está registrado."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # Criar o usuário inativo
                user = User.objects.create_user(
                    username=email, email=email, password=password, first_name=name, is_active=False
                )

                # Gerar token único
                token = get_random_string(length=32)

                # Salvar o token no perfil do usuário
                user.profile.validation_token = token
                user.profile.save()

                # Construir URL para validação do e-mail
                validation_url = f"{settings.FRONTEND_BASE_URL}/validate-email/{token}"

                # Enviar e-mail de validação
                send_mail(
                    subject="Valide seu registro",
                    message=f"Por favor, clique no link para validar sua conta: {validation_url}",
                    from_email="no-reply@licitacao360.com",
                    recipient_list=[email],
                )

            # Retornar sucesso
            return Response(
                {"message": "Usuário registrado com sucesso. Verifique seu e-mail para validar."},
                status=status.HTTP_201_CREATED,
            )

        except IntegrityError:
            return Response(
                {"error": "Erro ao salvar o usuário no banco de dados."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": f"Erro no registro: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def options(self, request, *args, **kwargs):
        # Apenas deixe o middleware lidar com CORS
        return Response(status=status.HTTP_200_OK)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"detail": "Use POST to send email and password."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def post(self, request):
        logger.info("Dados recebidos: %s", request.data)

        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            logger.warning("Email ou senha ausente.")
            return Response({'detail': 'Email e senha são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)
        if user:
            logger.info("Usuário autenticado: %s", email)
            refresh = RefreshToken.for_user(user)
            return Response({
                'name': user.username,
                'token': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        logger.warning("Credenciais inválidas para: %s", email)
        return Response({'detail': 'Credenciais inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)


import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from django.shortcuts import render
from django.http import JsonResponse
from .models import ControleContratos
from datetime import datetime
from django.db import connection

def criar_tabela_uasg(uasg):
    table_name = f"controle_{uasg}"
    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
        cursor.execute(f"""
            CREATE TABLE {table_name} (
                id SERIAL PRIMARY KEY,
                numero VARCHAR(50),
                tipo VARCHAR(50),
                processo VARCHAR(50),
                receita_despesa VARCHAR(20),
                subtipo VARCHAR(100),
                objeto TEXT,
                situacao VARCHAR(50),
                prorrogavel VARCHAR(10),
                categoria VARCHAR(50),
                subcategoria VARCHAR(50),
                data_assinatura DATE,
                data_publicacao DATE,
                vigencia_inicio DATE,
                vigencia_fim DATE,
                valor_inicial NUMERIC(15,2),
                valor_global NUMERIC(15,2),
                fornecedor_nome VARCHAR(255),
                fornecedor_cnpj VARCHAR(18),
                orgao_nome VARCHAR(255),
                unidade_gestora VARCHAR(255),
                link_historico TEXT
            );
        """)
    print(f"Tabela {table_name} criada com sucesso!")

def parse_decimal(value):
    """
    Converte valores numéricos no formato brasileiro (1.234,56) 
    para o formato esperado pelo PostgreSQL (1234.56).
    """
    if value:
        try:
            # Remove os pontos (milhares) e troca a vírgula por ponto (decimal)
            return float(value.replace('.', '').replace(',', '.'))
        except ValueError:
            print(f"Erro ao converter o valor: {value}")
            return 0.0
    return 0.0


# Função para buscar dados da API com retry
def get_api_data(url):
    session = requests.Session()
    retry = Retry(
        total=5,  # Número máximo de tentativas
        backoff_factor=1,  # Tempo entre tentativas (em segundos)
        status_forcelist=[500, 502, 503, 504],  # Códigos de erro para retry
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    print("Consultando a API...")
    response = session.get(url, headers={"accept": "application/json"}, timeout=10, verify=False)
    response.raise_for_status()  # Levanta erro se status não for 2xx
    print("Consulta à API concluída com sucesso!")
    return response.json()

from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
from datetime import datetime

logger = logging.getLogger(__name__)

def parse_decimal(value):
    """Converte valores no formato brasileiro para o formato do PostgreSQL."""
    if value:
        try:
            return float(value.replace('.', '').replace(',', '.'))
        except ValueError:
            logger.warning("Erro ao converter valor: %s", value)
    return None

@csrf_exempt
def consulta_api(request):
    def get_table_list():
        """Obtém todas as tabelas disponíveis que começam com 'controle_'."""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT tablename 
                FROM pg_tables 
                WHERE schemaname = 'public' AND tablename LIKE 'controle_%'
            """)
            return [row[0] for row in cursor.fetchall()]

    if request.method == 'POST':
        try:
            # Parse do corpo da requisição
            body = json.loads(request.body.decode('utf-8'))
            uasg = body.get('uasg')
            if not uasg:
                logger.warning("Código UASG não fornecido.")
                return JsonResponse({'success': False, 'message': 'Código UASG não fornecido.'}, status=400)

            logger.info("Código UASG recebido: %s", uasg)

            # URL da API externa
            api_url = f"https://contratos.comprasnet.gov.br/api/contrato/ug/{uasg}"

            # Configurar sessão com retries
            session = requests.Session()
            retry = Retry(
                total=5,
                backoff_factor=1,
                status_forcelist=[500, 502, 503, 504],
                allowed_methods=["GET"],
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount("https://", adapter)

            # Consulta à API externa
            response = session.get(api_url, headers={"accept": "application/json"}, timeout=10, verify=False)
            response.raise_for_status()
            data = response.json()

            # Criar tabela e armazenar dados
            criar_tabela_uasg(uasg)
            table_name = f"controle_{uasg}"
            with connection.cursor() as cursor:
                for item in data:
                    cursor.execute(f"""
                        INSERT INTO {table_name} (
                            numero, tipo, processo, receita_despesa, subtipo, objeto,
                            situacao, prorrogavel, categoria, subcategoria,
                            data_assinatura, data_publicacao, vigencia_inicio, vigencia_fim,
                            valor_inicial, valor_global, fornecedor_nome, fornecedor_cnpj,
                            orgao_nome, unidade_gestora, link_historico
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        item.get("numero"), item.get("tipo"), item.get("processo"), item.get("receita_despesa"),
                        item.get("subtipo"), item.get("objeto"), item.get("situacao"), item.get("prorrogavel"),
                        item.get("categoria"), item.get("subcategoria"),
                        datetime.strptime(item.get("data_assinatura"), "%Y-%m-%d").date() if item.get("data_assinatura") else None,
                        datetime.strptime(item.get("data_publicacao"), "%Y-%m-%d").date() if item.get("data_publicacao") else None,
                        datetime.strptime(item.get("vigencia_inicio"), "%Y-%m-%d").date() if item.get("vigencia_inicio") else None,
                        datetime.strptime(item.get("vigencia_fim"), "%Y-%m-%d").date() if item.get("vigencia_fim") else None,
                        parse_decimal(item.get("valor_inicial")),
                        parse_decimal(item.get("valor_global")),
                        item["fornecedor"].get("nome"),
                        item["fornecedor"].get("cnpj_cpf_idgener"),
                        item["contratante"]["orgao"].get("nome"),
                        item["contratante"]["orgao"]["unidade_gestora"].get("nome"),
                        item["links"].get("historico"),
                    ))
            return JsonResponse({'success': True, 'message': f"Tabela {table_name} criada e atualizada com sucesso."})

        except requests.RequestException as e:
            logger.error("Erro ao consultar API externa: %s", e)
            return JsonResponse({'success': False, 'message': f"Erro ao consultar API externa: {str(e)}"}, status=500)
        except Exception as e:
            logger.error("Erro ao processar dados: %s", e)
            return JsonResponse({'success': False, 'message': f"Erro ao processar dados: {str(e)}"}, status=500)

    elif request.method == 'GET':
        tabela = request.GET.get('tabela')
        if tabela:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tabela}'")
                    columns = [row[0] for row in cursor.fetchall()]

                    cursor.execute(f"SELECT * FROM {tabela}")
                    data = cursor.fetchall()

                return JsonResponse({'success': True, 'columns': columns, 'data': data})
            except Exception as e:
                logger.error("Erro ao recuperar dados da tabela: %s", e)
                return JsonResponse({'success': False, 'message': f"Erro ao recuperar dados: {str(e)}"}, status=500)

        # Retornar lista de tabelas disponíveis
        return JsonResponse({'success': True, 'tables': get_table_list()})

    logger.warning("Método não permitido: %s", request.method)
    return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)



# Função para buscar dados da API com retry
def get_api_data(url):
    session = requests.Session()
    retry = Retry(
        total=5,  # Número máximo de tentativas
        backoff_factor=1,  # Tempo entre tentativas (em segundos)
        status_forcelist=[500, 502, 503, 504],  # Códigos de erro para retry
        allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    print("Consultando a API...")
    response = session.get(url, headers={"accept": "application/json"}, timeout=10, verify=False)
    response.raise_for_status()  # Levanta erro se status não for 2xx
    print("Consulta à API concluída com sucesso!")
    return response.json()

def limpar_tabelas(request):
    """Remove todas as tabelas cujo nome começa com 'consulta_'."""
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                # Buscar todas as tabelas que começam com 'consulta_'
                cursor.execute("""
                    SELECT tablename 
                    FROM pg_tables 
                    WHERE schemaname = 'public' AND tablename LIKE 'consulta_%'
                """)
                tabelas = [row[0] for row in cursor.fetchall()]

                # Deletar as tabelas encontradas
                for tabela in tabelas:
                    cursor.execute(f"DROP TABLE IF EXISTS {tabela} CASCADE;")
                return JsonResponse({'success': True, 'message': f"{len(tabelas)} tabelas removidas com sucesso!"})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Método inválido!'})
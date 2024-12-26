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
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import logging
import requests
from requests.adapters import HTTPAdapter, Retry
import json
from datetime import datetime
from api.utils import parse_decimal, get_table_list
from .save_model import salvar_dados_no_model

logger = logging.getLogger(__name__)

from django.db import connection

def limpar_tabela_uasg(uasg):
    table_name = f"app_contratos_controlecomprasnetcontratos"
    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        print(f"Tabela {table_name} foi removida com sucesso.")

def criar_tabela_uasg(uasg):
    table_name = f"app_contratos_controlecomprasnetcontratos"
    with connection.cursor() as cursor:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
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
                valor_inicial NUMERIC(15, 2),
                valor_global NUMERIC(15, 2),
                fornecedor_nome VARCHAR(255),
                fornecedor_cnpj VARCHAR(18),
                codigo_orgao VARCHAR(50),
                orgao_nome VARCHAR(255),
                uasg VARCHAR(6),
                sigla_uasg VARCHAR(50),
                unidade_gestora VARCHAR(255),
                link_historico TEXT,
                link_empenhos TEXT,
                link_garantias TEXT,
                link_itens TEXT,
                link_prepostos TEXT,
                link_responsaveis TEXT,
                link_faturas TEXT,
                link_ocorrencias TEXT,
                link_arquivos TEXT
            );
        """)
    return table_name

def deletar_tabela_uasg(uasg):
    table_name = f"app_contratos_controlecomprasnetcontratos"
    with connection.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    return table_name

from django.http import JsonResponse
import requests

def proxy_download(request, contrato_id):
    url = f"https://contratos.comprasnet.gov.br/api/contrato/{contrato_id}/arquivos"
    try:
        # Faz a requisição ao endpoint externo
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Verifica se há um path_arquivo nos dados retornados
        if not data or not any("path_arquivo" in item for item in data):
            return JsonResponse(
                {'error': 'Nenhum arquivo disponível para download.'},
                status=404
            )

        # Retorna os dados para o frontend
        return JsonResponse(data, safe=False)

    except requests.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

        
def consulta_comprasnetcontratos(request):
    logger.info("Consulta recebida")
    uasg = request.GET.get('uasg')
    
    if not uasg:
        return JsonResponse({'success': False, 'message': 'Código UASG não fornecido.'}, status=400)

    try:
        api_url = f"https://contratos.comprasnet.gov.br/api/contrato/ug/{uasg}"
        session = requests.Session()
        retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504], allowed_methods=["GET"])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)

        # Consulta à API externa
        response = session.get(api_url, headers={"accept": "application/json"}, timeout=10, verify=True)

        if response.status_code != 200:
            logger.error(f"Erro na API externa: {response.status_code}")
            return JsonResponse({'success': False, 'message': f"Erro na API externa: {response.status_code}"}, status=500)

        try:
            data = response.json()
        except json.JSONDecodeError:
            logger.error("Erro ao processar resposta da API externa. JSON inválido.")
            return JsonResponse({'success': False, 'message': 'Erro ao processar resposta da API externa. JSON inválido.'}, status=500)

        if not data:
            logger.warning("A API retornou uma resposta vazia.")
            return JsonResponse({'success': False, 'message': 'A API retornou uma resposta vazia.', 'data': []}, status=404)


        # Processar contratos
        contratos = []
        for item in data:
            contrato = {
                "uasg": uasg,
                "numero": item.get("numero"),
                "tipo": item.get("tipo"),
                "processo": item.get("processo"),
                "receita_despesa": item.get("receita_despesa"),
                "subtipo": item.get("subtipo"),
                "objeto": item.get("objeto"),
                "situacao": item.get("situacao"),
                "prorrogavel": item.get("prorrogavel"),
                "categoria": item.get("categoria"),
                "subcategoria": item.get("subcategoria"),
                "data_assinatura": item.get("data_assinatura"),
                "data_publicacao": item.get("data_publicacao"),
                "vigencia_inicio": item.get("vigencia_inicio"),
                "vigencia_fim": item.get("vigencia_fim"),
                "valor_inicial": item.get("valor_inicial"),
                "valor_global": item.get("valor_global"),
                "fornecedor_nome": item.get("fornecedor", {}).get("nome"),
                "fornecedor_cnpj": item.get("fornecedor", {}).get("cnpj_cpf_idgener"),
                "codigo_orgao": item.get("contratante", {}).get("orgao", {}).get("codigo"),
                "orgao_nome": item.get("contratante", {}).get("orgao", {}).get("nome"),
                "sigla_uasg": item.get("contratante", {}).get("sigla"),
                "unidade_gestora": item.get("contratante", {}).get("orgao", {}).get("unidade_gestora", {}).get("nome"),
                "link_historico": item.get("links", {}).get("historico"),
                "link_empenhos": item.get("links", {}).get("empenhos"),
                "link_garantias": item.get("links", {}).get("garantias"),
                "link_itens": item.get("links", {}).get("itens"),
                "link_prepostos": item.get("links", {}).get("prepostos"),
                "link_responsaveis": item.get("links", {}).get("responsaveis"),
                "link_faturas": item.get("links", {}).get("faturas"),
                "link_ocorrencias": item.get("links", {}).get("ocorrencias"),
                "link_arquivos": item.get("links", {}).get("arquivos"),
            }
            contratos.append(contrato)
            print(f"Contrato processado: {contrato}")  # Verificar cada contrato processado

        # Salvar os dados no banco de dados
        print(f"Total de contratos processados: {len(contratos)}")
        salvar_dados_no_model(contratos)

        return JsonResponse({
            'success': True,
            'message': f"Dados da UASG {uasg} salvos com sucesso.",
            'data': contratos
        })

    except Exception as e:
        logger.error("Erro ao processar dados: %s", e)
        return JsonResponse({'success': False, 'message': f"Erro ao processar dados: {str(e)}"}, status=500)


def metodo_nao_permitido(metodo):
    logger.warning(f"Método não permitido: {metodo}")
    return JsonResponse({'success': False, 'message': 'Método não permitido.'}, status=405)


def obter_parametro_uasg(request):
    uasg = request.GET.get('uasg')
    if not uasg:
        logger.warning("Código UASG não fornecido.")
    else:
        logger.info(f"Código UASG recebido: {uasg}")
    return uasg


def consultar_api_externa(uasg):
    api_url = f"https://contratos.comprasnet.gov.br/api/contrato/ug/{uasg}"
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504], allowed_methods=["GET"])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)

    logger.info(f"Consultando API externa: {api_url}")
    response = session.get(api_url, headers={"accept": "application/json"}, timeout=10, verify=True)
    logger.info(f"Status da API: {response.status_code}")
    return response


def processar_resposta_api(response):
    try:
        data = response.json()
        logger.info(f"Resposta da API processada com sucesso.")
        return data
    except Exception as e:
        logger.error(f"Erro ao decodificar JSON: {e}")
        raise


def inserir_dados_na_tabela(tabela_nome, data):
    # Implemente a lógica de inserção dos dados na tabela
    logger.info(f"Inserindo dados na tabela {tabela_nome}.")
    for item in data:
        logger.info(f"Inserindo contrato: {item.get('numero')}")
        # Implemente a lógica de inserção aqui
        pass
    
    
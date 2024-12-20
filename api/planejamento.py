from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Planejamento  # Substitua pelo modelo correto
from django.db import connection


@csrf_exempt
def adicionar_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tabela = data.get('tabela')
            novo_item = data.get('data')

            with connection.cursor() as cursor:
                # Substitua pela lógica do banco de dados
                cursor.execute(
                    f"INSERT INTO {tabela} ({', '.join(novo_item.keys())}) VALUES ({', '.join(['%s'] * len(novo_item))})",
                    list(novo_item.values())
                )

            return JsonResponse({'success': True, 'message': 'Item adicionado com sucesso.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

@csrf_exempt
def excluir_item(request, tabela, item_id):
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM {tabela} WHERE id = %s", [item_id])

            return JsonResponse({'success': True, 'message': 'Item excluído com sucesso.'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def gerar_tabela(request):
    if request.method == 'GET':
        try:
            tabela = request.GET.get('tabela')

            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {tabela}")
                rows = cursor.fetchall()

            return JsonResponse({'success': True, 'data': rows})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

def controlar_itens(request):
    if request.method == 'GET':
        try:
            tabela = request.GET.get('tabela')

            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {tabela}")
                rows = cursor.fetchall()

            return JsonResponse({'success': True, 'data': rows})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

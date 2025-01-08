from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import controlecomprasnetcontratos, Comentario
from .serializers import ContratoSerializer, ComentarioSerializer

class ContratosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unidade_compra = request.query_params.get('unidade_compra')
        if not unidade_compra:
            return Response({"error": "UASG é obrigatório."}, status=400)

        # Filtra os dados pelo campo UASG
        contratos = controlecomprasnetcontratos.objects.filter(unidade_compra=unidade_compra)
        serializer = ContratoSerializer(contratos, many=True)

        return Response({"data": serializer.data}, status=200)

    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import controlecomprasnetcontratos
from .serializers import controlecomprasnetcontratosSerializer
import requests  # Para realizar chamadas à API externa
from django.db import IntegrityError
from django.apps import apps

class UpdateComprasnetContratosView(APIView):
    MAX_RETRIES = 5

    def post(self, request, *args, **kwargs):
        unidade_compra = getattr(request.user.profile, 'unidade_compra', None)
        if not unidade_compra:
            return Response(
                {"success": False, "message": "unidade_compra não encontrada para o usuário autenticado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        api_url = f"https://contratos.comprasnet.gov.br/api/contrato/ug/{unidade_compra}"
        print(f"Consultando API externa: {api_url}")

        for attempt in range(1, self.MAX_RETRIES + 1):
            try:
                # Chamada para a API externa
                response = requests.get(api_url, timeout=10)
                response.raise_for_status()
                contratos = response.json()

                if not contratos:
                    return Response(
                        {"success": False, "message": "Nenhum contrato encontrado na API externa."},
                        status=status.HTTP_404_NOT_FOUND
                    )

                valid_fields = [field.name for field in controlecomprasnetcontratos._meta.fields]
                contratos_criados, contratos_atualizados = 0, 0

                for contrato in contratos:
                    filtered_contrato = {key: value for key, value in contrato.items() if key in valid_fields}
                    codigo_orgao = contrato.get("contratante", {}).get("orgao", {}).get("codigo")
                    filtered_contrato["codigo_orgao"] = codigo_orgao.strip() if codigo_orgao else None

                    fornecedor_nome = contrato.get("fornecedor", {}).get("nome")
                    filtered_contrato["fornecedor_nome"] = fornecedor_nome.strip() if fornecedor_nome else None
                    
                    fornecedor_cnpj = contrato.get("fornecedor", {}).get("cnpj_cpf_idgener")
                    filtered_contrato["fornecedor_cnpj"] = fornecedor_cnpj.strip() if fornecedor_cnpj else None

                    filtered_contrato["vigencia_fim"] = contrato.get("vigencia_fim") or contrato.get("vigencia_inicio") or "9999-12-31"
                    filtered_contrato["valor_acumulado"] = filtered_contrato.get("valor_acumulado", 0)

                    for key in ["valor_global", "valor_inicial", "valor_parcela", "valor_acumulado"]:
                        if key in filtered_contrato and isinstance(filtered_contrato[key], str):
                            filtered_contrato[key] = self.convert_to_decimal(filtered_contrato[key])
                            
                    if not filtered_contrato.get("numero") or not filtered_contrato.get("unidade_compra"):
                        print(f"Contrato ignorado devido a dados incompletos: {filtered_contrato}")
                        continue

                    try:
                        obj, created = controlecomprasnetcontratos.objects.update_or_create(
                            numero=filtered_contrato.get("numero", "").strip(),
                            unidade_compra=filtered_contrato.get("unidade_compra", "").strip(),
                            defaults=filtered_contrato,
                        )
                        if created:
                            contratos_criados += 1
                        else:
                            contratos_atualizados += 1
                    except IntegrityError as e:
                        print(f"Erro de chave duplicada para contrato {filtered_contrato['numero']}, unidade {filtered_contrato['unidade_compra']}: {e}")
                        continue


                return Response(
                    {
                        "success": True,
                        "message": "Dados atualizados com sucesso.",
                        "created": contratos_criados,
                        "updated": contratos_atualizados,
                        "attempts": attempt
                    },
                    status=status.HTTP_200_OK
                )

            except requests.exceptions.RequestException as e:
                print(f"Tentativa {attempt} falhou: {e}")
                if attempt == self.MAX_RETRIES:
                    return Response(
                        {"success": False, "error": "Erro ao consultar API externa após várias tentativas."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )

            except Exception as e:
                print(f"Erro ao atualizar contratos: {e}")
                return Response(
                    {"success": False, "error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

    @staticmethod
    def convert_to_decimal(value):
        try:
            decimal_value = float(value.replace('.', '').replace(',', '.'))
            if decimal_value > 9999999999999.99:  # Limite para max_digits=15, decimal_places=2
                print(f"Valor excede o limite permitido: {value}")
                return None
            return decimal_value
        except ValueError:
            print(f"Valor inválido para conversão: {value}")
            return None
        
class ComentariosAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                comentario = Comentario.objects.get(pk=pk)
                serializer = ComentarioSerializer(comentario)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Comentario.DoesNotExist:
                return Response({"error": "Comentário não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            numero = request.query_params.get('numero')
            unidade_compra = request.query_params.get('unidade_compra')

            if not numero or not unidade_compra:
                return Response({"error": "Parâmetros 'numero' e 'unidade_compra' são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

            comentarios = Comentario.objects.filter(numero=numero, unidade_compra=unidade_compra)
            serializer = ComentarioSerializer(comentarios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            comentario = Comentario.objects.get(pk=pk)
        except Comentario.DoesNotExist:
            return Response({"error": "Comentário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ComentarioSerializer(comentario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            comentario = Comentario.objects.get(pk=pk)
        except Comentario.DoesNotExist:
            return Response({"error": "Comentário não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        comentario.delete()
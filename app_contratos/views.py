from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import controlecomprasnetcontratos
from .serializers import ContratoSerializer

class ContratosAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        uasg = request.query_params.get('uasg')
        if not uasg:
            return Response({"error": "UASG é obrigatório."}, status=400)

        # Filtra os dados pelo campo UASG
        contratos = controlecomprasnetcontratos.objects.filter(uasg=uasg)
        serializer = ContratoSerializer(contratos, many=True)

        return Response({"data": serializer.data}, status=200)

    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import controlecomprasnetcontratos
from .serializers import controlecomprasnetcontratosSerializer
import requests  # Para realizar chamadas à API externa
from django.apps import apps

class UpdateComprasnetContratosView(APIView):
    MAX_RETRIES = 5

    def post(self, request, *args, **kwargs):
        uasg = getattr(request.user.profile, 'uasg', None)
        if not uasg:
            return Response(
                {"success": False, "message": "UASG não encontrada para o usuário autenticado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        api_url = f"https://contratos.comprasnet.gov.br/api/contrato/ug/{uasg}"
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

                    uasg = contrato.get("contratante", {}).get("orgao", {}).get("unidade_gestora", {}).get("codigo")
                    filtered_contrato["uasg"] = uasg.strip() if uasg else None

                    fornecedor_nome = contrato.get("fornecedor", {}).get("nome")
                    filtered_contrato["fornecedor_nome"] = fornecedor_nome.strip() if fornecedor_nome else None
                    
                    fornecedor_cnpj = contrato.get("fornecedor", {}).get("cnpj_cpf_idgener")
                    filtered_contrato["fornecedor_cnpj"] = fornecedor_cnpj.strip() if fornecedor_cnpj else None

                    for key in ["valor_global", "valor_inicial", "valor_parcela", "valor_acumulado"]:
                        if key in filtered_contrato and isinstance(filtered_contrato[key], str):
                            filtered_contrato[key] = self.convert_to_decimal(filtered_contrato[key])

                    obj, created = controlecomprasnetcontratos.objects.update_or_create(
                        numero=filtered_contrato["numero"],
                        uasg=filtered_contrato["uasg"],
                        defaults=filtered_contrato,
                    )
                    if created:
                        contratos_criados += 1
                    else:
                        contratos_atualizados += 1

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
            return float(value.replace('.', '').replace(',', '.'))
        except ValueError:
            print(f"Valor inválido para conversão: {value}")
            return None

from rest_framework.viewsets import ModelViewSet
from ...models import ControleProcessos
from ...serializer import ControleProcessosSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)
class PlanejamentoListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        data = ControleProcessos.objects.all()
        serializer = ControleProcessosSerializer(data, many=True)
        return Response({'data': serializer.data})
    
class ConsultaApiView(APIView):
    def get(self, request, *args, **kwargs):
        tabela = request.query_params.get('tabela')
        if tabela == 'planejamento':
            # Adicione lógica para retornar os dados da tabela "planejamento"
            return Response({'data': []}, status=status.HTTP_200_OK)
        return Response({'error': 'Tabela não encontrada'}, status=status.HTTP_404_NOT_FOUND)

import logging
logger = logging.getLogger(__name__)

class ControleProcessosViewSet(ModelViewSet):
    queryset = ControleProcessos.objects.all()
    serializer_class = ControleProcessosSerializer

    def create(self, request, *args, **kwargs):
        logger.info(f"Dados recebidos: {request.data}")
        return super().create(request, *args, **kwargs)

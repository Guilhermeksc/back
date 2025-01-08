from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import Comentario
from ...serializer import ComentarioSerializer

class ComentariosAPIView(APIView):
    def get(self, request):
        numero = request.query_params.get('numero')
        unidade_compra = request.query_params.get('unidade_compra')

        if not numero or not unidade_compra:
            return Response({'error': 'Parâmetros inválidos.'}, status=status.HTTP_400_BAD_REQUEST)

        comentarios = Comentario.objects.filter(numero=numero, unidade_compra=unidade_compra)
        serializer = ComentarioSerializer(comentarios, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # 'atualizado_em' será preenchido automaticamente
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        comentario = Comentario.objects.get(pk=pk)
        serializer = ComentarioSerializer(comentario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comentario = Comentario.objects.get(pk=pk)
        comentario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

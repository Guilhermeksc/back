# app_contratos/urls.py

from django.urls import path
from .views import ContratosAPIView, UpdateComprasnetContratosView, ComentariosAPIView

urlpatterns = [
    path('', ContratosAPIView.as_view(), name='comprasnet_contratos'),
    path('update-comprasnet-contratos/', UpdateComprasnetContratosView.as_view(), name='update_comprasnet_contratos'),
    path('comentarios/', ComentariosAPIView.as_view(), name='comentarios'),

]

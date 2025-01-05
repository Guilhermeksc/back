from django.urls import path
from .views import ContratosAPIView, UpdateComprasnetContratosView

urlpatterns = [
    path('', ContratosAPIView.as_view(), name='comprasnet_contratos'),
    path('update-comprasnet-contratos/', UpdateComprasnetContratosView.as_view(), name='update_comprasnet_contratos'),
]

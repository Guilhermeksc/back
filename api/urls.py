# api/urls.py

from django.urls import path, include
from api.views.auth import *
from api.views.email_validation import ValidateEmailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import consulta_comprasnet_contratos, proxy_download
from .views import ComentariosAPIView, ChangePasswordView, ConsultaApiView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('consulta_comprasnet_contratos/', consulta_comprasnet_contratos, name='consulta_comprasnet_contratos'),
    path('validate-email/<str:token>/', ValidateEmailView.as_view(), name='validate-email'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('comentarios/', ComentariosAPIView.as_view(), name='comentarios'),
    path('comentarios/<int:pk>/', ComentariosAPIView.as_view(), name='comentarios-detail'),
    path('proxy/contrato/<int:contrato_id>/arquivos/', proxy_download, name='proxy_download'),
    path('consulta_api/', ConsultaApiView.as_view(), name='consulta_api'),

    # Inclua todas as rotas do app_contratos em um namespace
    path('comprasnet-contratos/', include('app_contratos.urls')),

    # Inclui as rotas de planejamento
    path('', include('app_planejamento.urls')),
]
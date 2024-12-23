from django.urls import path
<<<<<<< HEAD
from .views import (
    FrontendAppView,
    RegisterView,
    LoginView,
    consulta_api,
    limpar_tabelas,
    adicionar_item,
    excluir_item,
    gerar_tabela,
    controlar_itens,
)

urlpatterns = [
    path('', FrontendAppView.as_view(), name='frontend'),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('consulta_api/', consulta_api, name='consulta_api'),
    path('limpar_tabelas/', limpar_tabelas, name='limpar_tabelas'),
    path('adicionar_item/', adicionar_item, name='adicionar_item'),
    path('excluir_item/<str:tabela>/<int:item_id>/', excluir_item, name='excluir_item'),
    path('gerar_tabela/', gerar_tabela, name='gerar_tabela'),
    path('controlar_itens/', controlar_itens, name='controlar_itens'),
=======
from api.views import FrontendAppView, LoginView, RegisterView, PasswordResetView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views 
from .views import ValidateEmailView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('consulta_api/', views.consulta_api, name='consulta_api'),
    path('limpar_tabelas/', views.limpar_tabelas, name='limpar_tabelas'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password-reset/', SendPasswordResetLinkView.as_view(), name='send-reset-link'),
    path('reset-password/<str:token>/', ResetPasswordView.as_view(), name='reset-password'),
    path('validate-email/<str:token>/', ValidateEmailView.as_view(), name='validate-email'),
>>>>>>> recovery-branch
]

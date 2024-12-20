from django.urls import path
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
]

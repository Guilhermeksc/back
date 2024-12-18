from django.urls import path
from .views import FrontendAppView, RegisterView, LoginView
from . import views 

urlpatterns = [
    path('', FrontendAppView.as_view(), name='frontend'),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('consulta_api/', views.consulta_api, name='consulta_api'),
    path('limpar_tabelas/', views.limpar_tabelas, name='limpar_tabelas'),
]
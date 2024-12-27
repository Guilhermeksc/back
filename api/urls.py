# api/urls.py

from django.urls import path
from api.views.auth import LoginView, RegisterView
from api.views.email_validation import ValidateEmailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views.utils import consulta_api, limpar_tabelas


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('consulta_api/', consulta_api, name='consulta_api'),
    path('limpar_tabelas/', limpar_tabelas, name='limpar_tabelas'),
    path('validate-email/<str:token>/', ValidateEmailView.as_view(), name='validate-email'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

from django.urls import path
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
]

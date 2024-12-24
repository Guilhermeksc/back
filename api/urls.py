from django.urls import path
from api.views import FrontendAppView, LoginView, RegisterView, ChangePasswordView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views 
from .views import ValidateEmailView, SendPasswordResetLinkView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('consulta_api/', views.consulta_api, name='consulta_api'),
    path('limpar_tabelas/', views.limpar_tabelas, name='limpar_tabelas'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('validate-email/<str:token>/', ValidateEmailView.as_view(), name='validate-email'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

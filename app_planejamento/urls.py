# app_planejamento/urls.py

from rest_framework.routers import DefaultRouter
from .views import ControleProcessosViewSet

router = DefaultRouter()
router.register(r'controle-processos', ControleProcessosViewSet, basename='controle-processos')

urlpatterns = router.urls

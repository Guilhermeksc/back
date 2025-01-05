## backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')), 
    path('planejamento/', include('app_planejamento.urls')),
    path('comprasnet-contratos/', include('app_contratos.urls'))
]
    
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]    
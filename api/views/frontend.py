from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import Http404
from django.conf import settings
import os

def index(request):
    return render(request, 'index.html') 


class FrontendAppView(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        template_path = os.path.join(settings.TEMPLATES[0]['DIRS'][0], self.template_name)
        if not os.path.exists(template_path):
            raise Http404(f"Template não encontrado: {template_path}")
        return super().get(request, *args, **kwargs)

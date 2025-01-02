from django.contrib import admin
from .models import ControleProcessos

@admin.register(ControleProcessos)
class ControleProcessosAdmin(admin.ModelAdmin):
    list_display = ('id_processo', 'tipo', 'numero', 'ano', 'etapa', 'uasg', 'valor_total')
    list_filter = ('ano', 'etapa', 'uasg', 'situacao')
    search_fields = ('id_processo', 'objeto', 'uasg', 'nup')
    ordering = ('-ano', 'id_processo')
    list_editable = ('etapa', 'valor_total')
    list_per_page = 20

    # Personalizando o formulário de edição
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('id_processo', 'tipo', 'numero', 'ano', 'uasg')
        }),
        ('Detalhes do Processo', {
            'fields': ('situacao', 'etapa', 'material_servico', 'nup', 'objeto', 'valor_total'),
            'classes': ('collapse',),  # Colapsar esta seção
        }),
        ('Datas e Prazos', {
            'fields': ('data_sessao', 'vigencia', 'data_limite_entrega_tr'),
        }),
    )

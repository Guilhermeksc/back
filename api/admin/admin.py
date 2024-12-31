from django.contrib import admin
from ..models import ControleContratos
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(ControleContratos)
class ControleContratosAdmin(admin.ModelAdmin):
    list_display = (
        'numero', 
        'fornecedor_nome', 
        'fornecedor_cnpj', 
        'processo', 
        'tipo', 
        'subtipo', 
        'situacao', 
        'valor_global', 
        'data_assinatura', 
        'vigencia_inicio', 
        'vigencia_fim'
    )
    search_fields = ('numero', 'fornecedor_nome', 'fornecedor_cnpj', 'processo')
    list_filter = ('tipo', 'situacao', 'categoria', 'prorrogavel')
    readonly_fields = ('link_historico', 'link_empenhos', 'link_garantias', 'link_itens', 'link_prepostos', 'link_responsaveis', 'link_faturas', 'link_ocorrencias', 'link_arquivos',)
    ordering = ('data_assinatura',)

    fieldsets = (
        ("Informações Principais", {
            'fields': (
                ('numero', 'processo'),
                ('tipo', 'subtipo'),
                'situacao',
                'categoria',
                'prorrogavel',
            )
        }),
        ("Fornecedor", {
            'fields': (
                ('fornecedor_nome', 'fornecedor_cnpj'),
            )
        }),
        ("Datas", {
            'fields': (
                ('data_assinatura', 'data_publicacao'),
                ('vigencia_inicio', 'vigencia_fim'),
            )
        }),
        ("Valores", {
            'fields': (
                'valor_inicial',
                'valor_global',
                'valor_parcela',
                'valor_acumulado',
            )
        }),
        ("Links Externos", {
            'fields': (
                'link_historico',
                'link_empenhos',
                'link_faturas',
            )
        }),
    )

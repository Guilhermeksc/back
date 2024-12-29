from django.contrib import admin
from .models import ControleContratos
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Perfil"
    fields = ("uasg",)  # Apenas exibe o campo uasg

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_uasg",
    )

    def get_uasg(self, obj):
        return obj.profile.uasg
    get_uasg.short_description = "UASG"

# Re-registre o modelo User com o novo UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

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
    readonly_fields = ('link_historico', 'link_empenhos', 'link_cronograma', 'link_faturas')
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
                'link_cronograma',
                'link_faturas',
            )
        }),
    )

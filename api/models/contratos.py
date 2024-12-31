# api/models.py

from django.db import models

class ControleContratos(models.Model):
    uasg = models.CharField(max_length=10, default="000000", verbose_name="UASG")

    numero = models.CharField(max_length=50, verbose_name="Número")
    tipo = models.CharField(max_length=50, verbose_name="Tipo")
    processo = models.CharField(max_length=50, verbose_name="Processo")
    receita_despesa = models.CharField(max_length=20, verbose_name="Receita/Despesa")
    subtipo = models.CharField(max_length=100, null=True, verbose_name="Subtipo")
    objeto = models.TextField(verbose_name="Objeto")
    situacao = models.CharField(max_length=50, verbose_name="Situação")
    prorrogavel = models.CharField(max_length=10, null=True, blank=True, verbose_name="Prorrogável")

    categoria = models.CharField(max_length=50, verbose_name="Categoria")
    subcategoria = models.CharField(max_length=50, null=True, blank=True, verbose_name="Subcategoria")
    
    # Datas
    data_assinatura = models.DateField(null=True, blank=True, verbose_name="Data de Assinatura")
    data_publicacao = models.DateField(null=True, blank=True, verbose_name="Data de Publicação")

    vigencia_inicio = models.DateField(verbose_name="Início da Vigência")
    vigencia_fim = models.DateField(verbose_name="Fim da Vigência")

    # Valores
    valor_inicial = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Inicial")
    valor_global = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="Valor Global")
    valor_parcela = models.DecimalField(max_digits=15, decimal_places=2, null=True, verbose_name="Valor Parcela")
    valor_acumulado = models.DecimalField(max_digits=15, decimal_places=2, null=True, verbose_name="Valor Acumulado")

    # Informações do fornecedor
    fornecedor_nome = models.CharField(max_length=255, verbose_name="Nome do Fornecedor")
    fornecedor_cnpj = models.CharField(max_length=18, verbose_name="CNPJ do Fornecedor")

    # Informações da contratante
    codigo_orgao = models.CharField(max_length=50, null=True, blank=True, verbose_name="Código do Órgão")
    orgao_nome = models.CharField(max_length=255, verbose_name="Órgão Contratante")
    uasg = models.CharField(max_length=20, null=True, blank=True, verbose_name="UASG")
    sigla_uasg = models.CharField(max_length=50, null=True, blank=True, verbose_name="Sigla da UASG")
    unidade_gestora = models.CharField(max_length=255, verbose_name="Unidade Gestora")

    # Links externos
    link_historico = models.URLField(null=True, blank=True, verbose_name="Link Histórico")
    link_empenhos = models.URLField(null=True, blank=True, verbose_name="Link Empenhos")
    link_garantias = models.URLField(null=True, blank=True, verbose_name="Link Garantias")
    link_itens = models.URLField(null=True, blank=True, verbose_name="Link Itens")
    link_prepostos = models.URLField(null=True, blank=True, verbose_name="Link Prepostos")
    link_responsaveis = models.URLField(null=True, blank=True, verbose_name="Link Responsáveis")
    link_faturas = models.URLField(null=True, blank=True, verbose_name="Link Faturas")
    link_ocorrencias = models.URLField(null=True, blank=True, verbose_name="Link Ocorrências")
    link_arquivos = models.URLField(null=True, blank=True, verbose_name="Link Arquivos")


    def __str__(self):
        return f"{self.numero} - {self.uasg} - {self.fornecedor_nome}"

    class Meta:
        verbose_name = "Controle de Contrato"
        verbose_name_plural = "Controle de Contratos"
        ordering = ['uasg', 'numero']

def create_dynamic_model(uasg):
    table_name = f"controle_{uasg}"
    class Meta:
        db_table = table_name
        verbose_name = f"Controle {uasg}"
        verbose_name_plural = f"Controles {uasg}"
    
    attrs = {
        '__module__': __name__,
        'Meta': Meta,
        'id': models.AutoField(primary_key=True),
        'numero': models.CharField(max_length=50),
        'tipo': models.CharField(max_length=50),
        'processo': models.CharField(max_length=50),
        'receita_despesa': models.CharField(max_length=20),
        'subtipo': models.CharField(max_length=100),
        'objeto': models.TextField(),
        'situacao': models.CharField(max_length=50),
        'prorrogavel': models.CharField(max_length=10),
        'categoria': models.CharField(max_length=50),
        'subcategoria': models.CharField(max_length=50),
        'data_assinatura': models.DateField(),
        'data_publicacao': models.DateField(),
        'vigencia_inicio': models.DateField(),
        'vigencia_fim': models.DateField(),
        'valor_inicial': models.DecimalField(max_digits=15, decimal_places=2),
        'valor_global': models.DecimalField(max_digits=15, decimal_places=2),
        'valor_parcela': models.DecimalField(max_digits=15, decimal_places=2),
        'valor_acumulado': models.DecimalField(max_digits=15, decimal_places=2),
        'fornecedor_nome': models.CharField(max_length=255),
        'fornecedor_cnpj': models.CharField(max_length=18),
        'orgao_nome': models.CharField(max_length=255),
        'unidade_gestora': models.CharField(max_length=255),
        'link_historico': models.URLField(),
        'link_empenhos': models.URLField(),
        'link_faturas': models.URLField(),
    }

    return type(table_name, (models.Model,), attrs)
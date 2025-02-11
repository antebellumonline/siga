# apps/centroProva/admin.py

"""
Configuração da interface administrativa para o app 'centroProva'.

Ele registra os modelos para que possam ser gerenciados através do painel administrativo do Django,
definindo quais campos serão exibidos, quais podem ser pesquisados, 
filtrados e quais são somente leitura.
"""

from django.contrib import admin
from .models import CentroProva, CentroProvaExame

@admin.register(CentroProva)
class CentroProvaAdmin(admin.ModelAdmin):
    """
    Configuração do modelo CentroProva no painel administrativo.

    Exibe os seguintes campos em formato de lista: ID, nome e status de inatividade.
    Permite pesquisar por nome.
    Permite filtrar os resultados por status de inatividade.
    """
    # Campos para exibição
    list_display = ('id', 'nome', 'inativo')
    # Campos para pesquisa
    search_fields = ('nome',)
    # Filtros para a lista
    list_filter = ('inativo',)

@admin.register(CentroProvaExame)
class CentroProvaExameAdmin(admin.ModelAdmin):
    """
    Configuração do modelo CentroProvaExame no painel administrativo.

    Exibe os seguintes campos em formato de lista: ID, certificação, centro de prova, aluno,
    data do exame, presença, status de cancelamento e status de inatividade.
    Permite pesquisar por certificação, aluno e centro de prova.
    Permite filtrar os resultados por presença, status de cancelamento e status de inatividade.
    """
    # Campos para exibição
    list_display = (
        'id', 
        'certificacao', 
        'centroProva', 
        'aluno', 
        'data', 
        'presenca', 
        'cancelado'
    )
    # Campos para pesquisa
    search_fields = ('certificacao__nome', 'centroProva__nome', 'aluno__nome')
    # Filtros para a lista
    list_filter = ('presenca', 'cancelado')

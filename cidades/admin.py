# apps/cidades/admin.py

"""
Este módulo configura a interface administrativa para o app de Cidades.
Ele registra os modelos para que possam ser gerenciados através do painel administrativo do Django.
"""

from django.contrib import admin
from .models import Estado, Cidade

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    """
    Configuração do modelo Estado no painel administrativo.
    """
    list_display = ('id', 'nome')
    search_fields = ('id', 'nome')  # Campos que podem ser pesquisados
    list_filter = ('id', 'nome')  # Filtros que podem ser aplicados
    readonly_fields = ('id',)  # Define id como somente leitura

@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    """
    Configuração do modelo Cidade no painel administrativo.
    """
    list_display = ('id', 'nome', 'estado')
    search_fields = ('id', 'nome')  # Campos que podem ser pesquisados
    list_filter = ('id', 'nome', 'estado')  # Filtros que podem ser aplicados
    readonly_fields = ('id',)  # Define id como somente leitura

"""
Este módulo configura a interface administrativa para o app de Alunos.
Ele registra os modelos para que possam ser gerenciados através do painel administrativo do Django.
"""

from django.contrib import admin
from .models import Aluno, ConfigTpContato, AlunoContato

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    """
    Configuração do modelo Aluno no painel administrativo.
    """
    list_display = ('uid', 'nome', 'cpf', 'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'observacao', 'inativo')
    search_fields = ('uid', 'nome', 'cpf', 'cidade')  # Campos que podem ser pesquisados
    list_filter = ('cidade', 'inativo')  # Filtros que podem ser aplicados
    readonly_fields = ('uid',)  # Define uid como somente leitura

@admin.register(ConfigTpContato)
class ConfigTpContatoAdmin(admin.ModelAdmin):
    """
    Configuração do modelo ConfigTpContato no painel administrativo.
    """
    list_display = ('id', 'descricao', 'inativo')

@admin.register(AlunoContato)
class AlunoContatoAdmin(admin.ModelAdmin):
    """
    Configuração do modelo AlunoContato no painel administrativo.
    """
    list_display = ('aluno', 'tipo_contato', 'contato', 'detalhe')

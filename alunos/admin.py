"""
Este módulo configura a interface administrativa para o app de Alunos.

Ele registra os modelos para que possam ser gerenciados através do painel administrativo do Django,
definindo quais campos serão exibidos, quais podem ser pesquisados, 
filtrados e quais são somente leitura.
"""

from django.contrib import admin
from .models import Aluno, ConfigTpContato, AlunoContato

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    """
    Configuração do modelo Aluno no painel administrativo.

    Exibe os seguintes campos em formato de lista: ID único, nome, CPF, CEP, endereço, número, 
    complemento, bairro, cidade, observação e status de inatividade.
    Permite pesquisar por ID, nome, CPF e cidade.
    Permite filtrar os resultados por cidade e status de inatividade.
    O campo 'uid' é definido como somente leitura, pois é gerado automaticamente.
    """
    # Campos para exibição
    list_display = (
        'uid', 
        'nome', 
        'cpf', 
        'cep', 
        'endereco', 
        'numero', 
        'complemento', 
        'bairro', 
        'cidade', 
        'observacao', 
        'inativo'
        )
    # Campos para pesquisa
    search_fields = ('uid', 'nome', 'cpf', 'cidade')
    # Filtros para a lista
    list_filter = ('cidade', 'inativo')
    # Campo somente leitura
    readonly_fields = ('uid',)

@admin.register(ConfigTpContato)
class ConfigTpContatoAdmin(admin.ModelAdmin):
    """
    Configuração do modelo ConfigTpContato no painel administrativo.

    Exibe o ID, a descrição e o status de inatividade dos tipos de contato.
    """
    list_display = ('id', 'descricao', 'inativo')

@admin.register(AlunoContato)
class AlunoContatoAdmin(admin.ModelAdmin):
    """
    Configuração do modelo AlunoContato no painel administrativo.

    Exibe o aluno relacionado, o tipo de contato, o contato em si e um detalhe adicional.
    """
    list_display = ('aluno', 'tipo_contato', 'contato', 'detalhe')

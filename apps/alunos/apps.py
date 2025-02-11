# apps/alunos/apps.py

"""
Configuração do aplicativo 'alunos' para a aplicação Django.

Define a configuração padrão e o nome do aplicativo.
"""

from django.apps import AppConfig

class AlunosConfig(AppConfig):
    """
    Classe de configuração para o aplicativo 'alunos'.
    Define o campo de chave primária padrão e o nome do aplicativo.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.alunos'

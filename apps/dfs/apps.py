# apps/dfs/apps.py

"""
Configuração do aplicativo 'dfs' para a aplicação Django.

Define a configuração padrão e o nome do aplicativo.
"""

from django.apps import AppConfig

class DfsConfig(AppConfig):
    """
    Classe de configuração para o aplicativo 'dfs'.
    Define o campo de chave primária padrão e o nome do aplicativo.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dfs'

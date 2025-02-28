# apps/cidades/apps.py

"""
Configuração do aplicativo 'cidades' para a aplicação Django.

Define a configuração padrão e o nome do aplicativo.
"""

from django.apps import AppConfig


class LocalidadesConfig(AppConfig):
    """
    Classe de configuração para o aplicativo 'cidades'.
    Define o campo de chave primária padrão e o nome do aplicativo.
    """
    name = 'apps.local'

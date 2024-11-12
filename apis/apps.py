# apis/apps.py

"""
Configuração do aplicativo 'apis' para a aplicação Django.

Define a configuração padrão e o nome do aplicativo.
"""

from django.apps import AppConfig


class ApisConfig(AppConfig):
    """
    Classe de configuração para o aplicativo 'apis'.
    Define o campo de chave primária padrão e o nome do aplicativo.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apis'

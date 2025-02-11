# apps/centroProva/apps.py

"""
Configuração do aplicativo 'centroProva' para a aplicação Django.

Define a configuração padrão e o nome do aplicativo.
"""

from django.apps import AppConfig

class CentroprovaConfig(AppConfig):
    """
    Classe de configuração para o aplicativo 'centroProva'.
    Define o campo de chave primária padrão e o nome do aplicativo.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.centroProva'

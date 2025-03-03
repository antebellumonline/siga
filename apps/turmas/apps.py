# apps/turmas/apps.py

"""
Configuração do aplicativo 'turmas' para a aplicação Django.

Define a configuração padrão e o nome do aplicativo.
"""

from django.apps import AppConfig

class TurmasConfig(AppConfig):
    """
    Classe de configuração para o aplicativo 'turmas'.
    Define o campo de chave primária padrão e o nome do aplicativo.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.turmas'

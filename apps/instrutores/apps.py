# apps/alunos/apps.py

"""
Configuração do aplicativo 'instrutores' para a aplicação Django.

Define a configuração padrão e o nome do aplicativo.
"""

from django.apps import AppConfig


class InstrutoresConfig(AppConfig):
    """
    Classe de configuração para o aplicativo 'instrutores'.
    Define o campo de chave primária padrão e o nome do aplicativo.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.instrutores'

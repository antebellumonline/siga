# apps/cursos/apps.py

"""
Configuração do aplicativo 'cursos' para a aplicação Django.

Define a configuração padrão e o nome do aplicativo.
"""

from django.apps import AppConfig

class CursosConfig(AppConfig):
    """
    Classe de configuração para o aplicativo 'cursos'.
    Define o campo de chave primária padrão e o nome do aplicativo.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cursos'

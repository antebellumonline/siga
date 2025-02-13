# apps/empresas/apps.py

"""
Configuração do aplicativo 'empresas' para a aplicação Django.

Define a configuração padrão e o nome do aplicativo.
"""

from django.apps import AppConfig

class EmpresasConfig(AppConfig):
    """
    Classe de configuração para o aplicativo 'empresas'.
    Define o campo de chave primária padrão e o nome do aplicativo.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'empresas'

#!/usr/bin/env python

"""
Este script inicializa a aplicação Django configurando o ambiente e executando
comandos de gerenciamento. Carrega variáveis de ambiente do arquivo .env e
configura o módulo de configurações do Django.
"""

import os
import sys
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siga.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

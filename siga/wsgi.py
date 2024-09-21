"""
Configuração WSGI para o projeto siga.

Este arquivo define a aplicação WSGI como uma variável de nível de módulo chamada `application`.
"""

import os
from django.core.wsgi import get_wsgi_application

# Define a variável de ambiente `DJANGO_SETTINGS_MODULE`
# para apontar para o arquivo de configurações do projeto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siga.settings')

# Obtém a aplicação WSGI usando a função `get_wsgi_application` do Django
application = get_wsgi_application()

"""
Django settings for your_project.

This module contains the settings for the Django project, including
configuration for the database, installed apps, middleware, and more.
"""

import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes;'
        },
    }
}


# Outras configurações do Django...

DEBUG = True  # Defina como False em produção

ALLOWED_HOSTS = ['*']  # Substitua '*' por domínios específicos em produção
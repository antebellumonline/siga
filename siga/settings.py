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
        'NAME': os.getenv('SQL_SERVER_DATABASE'),
        'USER': os.getenv('SQL_SERVER_USER'),
        'PASSWORD': os.getenv('SQL_SERVER_PASSWORD'),
        'HOST': os.getenv('SQL_SERVER_URL'),
        'PORT': '1433',  # Geralmente em branco para Azure SQL Database
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes;'
        },
    }
}


# Outras configurações do Django...

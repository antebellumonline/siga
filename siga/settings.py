"""
Django settings for your_project.

This module contains the settings for the Django project, including
configuration for the database, installed apps, middleware, and more.
"""

from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='1433'),
        'OPTIONS': {
            'driver': config('DB_DRIVER', default='ODBC Driver 17 for SQL Server'),
            'extra_params': 'Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;',
        },
    }
}


# Outras configurações do Django...

"""
Django settings for your_project.

This module contains the settings for the Django project, including
configuration for the database, installed apps, middleware, and more.
"""

from decouple import config

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT'),
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}

# Outras configurações do Django...

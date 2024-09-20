"""
Django settings for your_project.

This module contains the settings for the Django project, including
configuration for the database, installed apps, middleware, and more.
"""

import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Definição do BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuração do SECRET_KEY
SECRET_KEY = os.getenv('SECRET_KEY')

# Configuração de depuração (DEBUG) a partir do .env
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Configuração de Allowed Hosts (permitir domínios específicos em produção)
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Configuração do banco de dados
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

# Configuração dos aplicativos instalados
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'siga',
    'cidades',
    'alunos',
    # Adicione outros aplicativos aqui
]

# Configuração dos middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Middleware extra de segurança, ativado apenas em produção
if not DEBUG:
    MIDDLEWARE += [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.http.ConditionalGetMiddleware',
        'django.middleware.common.BrokenLinkEmailsMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
    ]

# Configuração dos templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuração das URLs
ROOT_URLCONF = 'siga.urls'

# Configuração do WSGI
WSGI_APPLICATION = 'siga.wsgi.application'

# Configuração de validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuração de login/logout
LOGIN_URL = 'login'  # Rota para página de login
LOGIN_REDIRECT_URL = 'home'  # Após o login, redireciona para 'home'
LOGOUT_REDIRECT_URL = 'login'  # Após o logout, redireciona para 'login'

# Configurações de depuração SQL
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}


# Configuração de linguagem e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = False
USE_L10N = False
USE_TZ = True

# Configuração de arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Configuração do STATIC_ROOT para produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Definições adicionais
DEBUG = True  # Defina como False em produção
ALLOWED_HOSTS = ['*']  # Substitua '*' por domínios específicos em produção

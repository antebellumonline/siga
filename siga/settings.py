# siga/settings.py

"""
Configurações do Django para o projeto siga.

Este módulo contém as configurações para o projeto Django siga, incluindo
configurações para o banco de dados, aplicativos instalados, middlewares e muito mais.
"""

import os
import pymysql
import environ
from django.db.backends.signals import connection_created
from django.dispatch import receiver

# Inicializa o pymysql
pymysql.install_as_MySQLdb()

# Inicializa o django-environ
env = environ.Env()
environ.Env.read_env()  # Lê o arquivo .env

# Definição do diretório base do projeto (BASE_DIR)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuração da chave secreta (SECRET_KEY)
SECRET_KEY = env('SECRET_KEY')

# Configuração do modo de depuração (DEBUG) baseado na variável de ambiente
DEBUG = env.bool('DEBUG', default=False)

# Configuração dos hosts permitidos (ALLOWED_HOSTS) para produção
ALLOWED_HOSTS = env(
    'ALLOWED_HOSTS',
    default='127.0.0.1,localhost' if DEBUG else 'siga-app.azurewebsites.net,siga.antebellum.com.br'
).split(',')

# Configuração das origens confiáveis para CSRF
CSRF_TRUSTED_ORIGINS = ['https://siga-app.azurewebsites.net', 'https://siga.antebellum.com.br']

# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# Configuração de cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',  # Endereço do servidor Memcached
    }
}

# Configuração de cache em memória para ambiente de desenvolvimento
if DEBUG:
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',  # Identificador único para o cache em memória
    }

# Configuração de sessão
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'  # O alias do cache definido anteriormente

# Configuração dos aplicativos instalados (INSTALLED_APPS)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'siga',
    'apps.alunos',
    'apps.cidades',
    'apps.certificacoes',
    'apps.centroProva',
    'apis',
    'reports',
]

# Configuração dos middlewares (MIDDLEWARE)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'siga.middleware.LoginRequiredMiddleware',
]

# Configuração dos templates (TEMPLATES)
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
        'libraries': {
                'custom_filters': 'templatetags.custom_filters',
            },
        },
    },
]

# Configuração da URL principal (ROOT_URLCONF)
ROOT_URLCONF = 'siga.urls'

# Configuração da aplicação WSGI (WSGI_APPLICATION)
WSGI_APPLICATION = 'siga.wsgi.application'

# Configuração de validação de senhas (AUTH_PASSWORD_VALIDATORS)
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

# Configuração de login/logout Microsoft
MICROSOFT = {
    'app_id': os.getenv('MICROSOFT_APP_ID'),
    'app_secret': os.getenv('MICROSOFT_APP_SECRET'),
    'redirect': os.getenv('MICROSOFT_REDIRECT'),
    'scopes': os.getenv('MICROSOFT_SCOPES').split(','),
    'authority': os.getenv('MICROSOFT_AUTHORITY'),
    'valid_email_domains': os.getenv('MICROSOFT_VALID_EMAIL_DOMAINS').split(','),
    'logout_uri': os.getenv('MICROSOFT_LOGOUT_URI')
}

# Configuração de login/logout
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'login'

# Configurações de logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_errors.log'),
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Configuração de linguagem e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'  # Mudei para horário de Brasília
USE_I18N = True  # Defina como True se você deseja usar a internacionalização
USE_L10N = True  # Defina como True se você deseja usar a localização
USE_TZ = True

# Configuração de arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'docs/build/html'),
]

# Configurações de Segurança
SESSION_COOKIE_SECURE = True  # Envia o cookie de sessão apenas por HTTPS
SESSION_COOKIE_HTTPONLY = True  # Impede que o cookie seja acessado via JavaScript
SESSION_COOKIE_SAMESITE = 'Lax'  # Reduz o risco de vazamento de cookies em requisições cross-site

# Configuração do STATIC_ROOT para produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

@receiver(connection_created)
def set_strict_mode(connection, **_):
    """
    Configura o modo SQL para STRICT_TRANS_TABLES e NO_ENGINE_SUBSTITUTION
    para melhorar a integridade dos dados no MariaDB.
    """
    with connection.cursor() as cursor:
        cursor.execute("SET SESSION sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION';")

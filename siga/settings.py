"""
Configurações do Django para o projeto siga.

Este módulo contém as configurações para o projeto Django siga, incluindo
configurações para o banco de dados, aplicativos instalados, middlewares e muito mais.
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Definição do diretório base do projeto (BASE_DIR)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuração da chave secreta (SECRET_KEY)
SECRET_KEY = os.getenv('SECRET_KEY')

# Configuração do modo de depuração (DEBUG) baseado na variável de ambiente
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Configuração dos hosts permitidos (ALLOWED_HOSTS) para produção
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if not DEBUG else ['*']

# Configuração do banco de dados
DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc', # Motor do banco de dados
        'NAME': os.getenv('DB_NAME'), # Nome do banco de dados
        'USER': os.getenv('DB_USER'), # Usuário do banco de dados
        'PASSWORD': os.getenv('DB_PASSWORD'), # Senha do banco de dados
        'HOST': os.getenv('DB_HOST'), # Host do banco de dados
        'PORT': os.getenv('DB_PORT'), # Porta do banco de dados
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server', # Driver ODBC para SQL Server
            'timeout': 300,  # Tempo limite de conexão em segundos
            # Parâmetros extras de conexão
            'extra_params': 'TrustServerCertificate=yes;MultiSubnetFailover=yes;',
        },
    }
}

# Configuração dos aplicativos instalados (INSTALLED_APPS)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fontawesome_free'
    'siga', # Aplicativo principal do projeto
    'cidades', # Aplicativo Cidades
    'alunos', #Aplicativo Alunos
    # Adicione outros aplicativos aqui
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
]

# Middleware extra de segurança ativados apenas em produção
if not DEBUG:
    MIDDLEWARE += [
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.http.ConditionalGetMiddleware',
        'django.middleware.common.BrokenLinkEmailsMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
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
        },
    },
]

# Configuração da URL principal (ROOT_URLCONFIG)
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
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Configuração do STATIC_ROOT para produção
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Definições adicionais
DEBUG = True  # Defina como False em produção
ALLOWED_HOSTS = ['*']  # Substitua '*' por domínios específicos em produção

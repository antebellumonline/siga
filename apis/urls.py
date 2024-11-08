# apps/apis/urls.py

"""
Definição das URLs para o aplicativo 'apis'.

Ele mapeia as requisições HTTP para as respectivas views, 
permitindo a navegação e interação com o sistema.
"""

from django.urls import path
from .views import busca_cep

urlpatterns = [
    path('busca-cep/', busca_cep, name='busca_cep'),
]

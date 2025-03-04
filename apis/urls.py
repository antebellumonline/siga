# apis/urls.py

"""
Definição das URLs para o aplicativo 'apis'.

Ele mapeia as requisições HTTP para as respectivas views, 
permitindo a navegação e interação com o sistema.
"""

from django.urls import path
from .import views

urlpatterns = [
    path('buscacep/<str:cep>/', views.busca_cep_view, name='busca_cep'),
    path('buscacnpj/<str:taxId>/', views.busca_cnpj_view, name='busca_cnpj'),
]

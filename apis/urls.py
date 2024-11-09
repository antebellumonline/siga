# apps/apis/urls.py

"""
Definição das URLs para o aplicativo 'apis'.

Ele mapeia as requisições HTTP para as respectivas views, 
permitindo a navegação e interação com o sistema.
"""

from django.urls import path
from .import views

urlpatterns = [
    path('buscacep/<str:cep>/', views.busca_cep, name='busca_cep'),
]

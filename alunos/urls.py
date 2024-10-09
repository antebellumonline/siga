# apps/alunos/urls.py

"""
Este módulo define as URLs para o aplicativo de alunos. 
Ele mapeia as requisições HTTP para as respectivas views, 
permitindo a navegação e interação com o sistema.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # URL para login
    path('', views.home, name='home'),  # URL para a página inicial (home)
    path('alunos/', views.aluno_home, name='aluno_home'),
    path('alunos/list', views.aluno_list, name='aluno_list'),
    path('aluno/<int:pk>/', views.aluno_detail, name='aluno_detail'),
    path('aluno/new/', views.aluno_new, name='aluno_new'),
    path('aluno/<int:pk>/edit/', views.aluno_update, name='aluno_update'),
    path('aluno/<int:pk>/delete/', views.aluno_delete, name='aluno_delete'),
    path('cidades/por-codigo-ibge/<str:codigo_ibge>/', views.cidade_por_codigo_ibge, name='cidade_por_codigo_ibge'),
]

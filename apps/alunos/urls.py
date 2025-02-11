# apps/alunos/urls.py

"""
Definição das URLs para o aplicativo 'alunos'.

Ele mapeia as requisições HTTP para as respectivas views, 
permitindo a navegação e interação com o sistema.
"""

from django.urls import path
from . import views

urlpatterns = [
    # URL página Principal do Centro de Provas
    path('alunos/', views.aluno_home, name='aluno_home'),

    # URLs Alunos
    path('aluno/new/', views.aluno_new, name='aluno_new'),
    path('alunos/list', views.aluno_list, name='aluno_list'),
    path('aluno/<int:pk>/', views.aluno_detail, name='aluno_detail'),
    path('aluno/<int:pk>/edit/', views.aluno_edit, name='aluno_edit'),
    path('aluno/<int:pk>/delete/', views.aluno_delete, name='aluno_delete'),
]

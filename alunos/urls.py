# apps/alunos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),  # URL para login
    path('', views.home, name='home'),  # URL para a página inicial (home)
    path('alunos/', views.aluno_list, name='aluno_list'),  # Corrigido para não conflitar com a URL raiz
    path('aluno/<int:pk>/', views.aluno_detail, name='aluno_detail'),
    path('aluno/new/', views.aluno_create, name='aluno_create'),
    path('aluno/<int:pk>/edit/', views.aluno_update, name='aluno_update'),
    path('aluno/<int:pk>/delete/', views.aluno_delete, name='aluno_delete'),
    path('cidades/por-codigo-ibge/<str:codigo_ibge>/', views.cidade_por_codigo_ibge, name='cidade_por_codigo_ibge'),
]

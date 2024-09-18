# apps/alunos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.aluno_list, name='aluno_list'),
    path('aluno/<int:pk>/', views.aluno_detail, name='aluno_detail'),
    path('aluno/new/', views.aluno_create, name='aluno_create'),
    path('aluno/<int:pk>/edit/', views.aluno_update, name='aluno_update'),
    path('aluno/<int:pk>/delete/', views.aluno_delete, name='aluno_delete'),
]

# apps/turmas/urls.py

"""
Definição das URLs para o aplicativo 'turmas'.
"""

from django.urls import path
from . import views

# URLs Turmas
urlpatterns = [
    path('turma/', views.turma_home, name='turma_home'),
    path('turma/new/', views.turma_new, name='turma_new'),
    path('turma/list/', views.turma_list, name='turma_list'),
    path('turma/<str:pk>/', views.turma_detail, name='turma_detail'),
    path('turma/<str:pk>/edit/', views.turma_edit, name='turma_edit'),
    path('turma/<str:pk>/delete/', views.turma_delete, name='turma_delete'),
]

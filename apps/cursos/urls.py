# apps/cursos/urls.py

"""
Definição das URLs para o aplicativo 'cursos'.

Ele mapeia as requisições HTTP para as respectivas views, 
permitindo a navegação e interação com o sistema.
"""

from django.urls import path
from . import views

urlpatterns = [
    #URL página Principal do App Cursos
    path(
        'curso/',
         views.curso_home,
         name='curso_home'
    ),

    # URLs Cursos
    path(
        'curso/new/',
        views.curso_new,
        name='curso_new'
    ),
    path(
        'curso/list/',
        views.curso_list,
        name='curso_list'
    ),
    path(
        'curso/<str:pk>/',
        views.curso_detail,
        name='curso_detail'
    ),
    path(
        'curso/<str:pk>/edit/',
        views.curso_edit,
        name='curso_edit'
    ),
    path(
        'curso/<str:pk>/delete/',
        views.curso_delete,
        name='curso_delete'
    ),

    # URLs Categoria de Cursos
    path(
        'curso/categoria/new/',
        views.cursocategoria_new,
        name='cursoCategoria_new'
    ),
    path(
        'curso/categoria/list/',
        views.cursocategoria_list,
        name='cursoCategoria_list'
    ),
    path(
        'curso/categoria/<str:sigla>/',
        views.cursocategoria_detail,
        name='cursoCategoria_detail'
    ),
    path(
        'curso/categoria/<str:sigla>/edit/',
        views.cursocategoria_edit,
        name='cursoCategoria_edit'
    ),
    path(
        'curso/categoria/<str:sigla>/delete/',
        views.cursocategoria_delete,
        name='cursoCategoria_delete'
    ),

    # URLs Training Blocks
    # path('curso/trainingBlocks/new/', views.trainingBlocks_new, name='trainingBlocks_new'),
    # path('curso/trainingBlocks/list/', views.trainingBlocks_list, name='trainingBlocks_list'),
    # path('curso/trainingBlocks/<int:pk>/', views.trainingBlocks_detail, name='trainingBlocks_detail'),
    # path('curso/trainingBlocks/<int:pk>/edit/', views.trainingBlocks_edit, name='trainingBlocks_edit'),
    # path('curso/trainingBlocks/<int:pk>/delete/', views.trainingBlocks_delete, name='trainingBlocks_delete'),
]

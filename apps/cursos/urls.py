# apps/cursos/urls.py

"""
Definição das URLs para o aplicativo 'cursos'.

Ele mapeia as requisições HTTP para as respectivas views, 
permitindo a navegação e interação com o sistema.
"""

from django.urls import path
from . import views

urlpatterns = [
    #URL páginas Iniciais
    path('curso/', views.curso_home, name='curso_home'),
    path('trainingBlocks/', views.trainingblocks_home, name='trainingblocks_home'),

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

    # URLs Tópicos Training Blocks
    path(
        'trainingBlocks/topico/new/',
        views.trainingblockstopico_new,
        name='trainingblockstopico_new'
    ),
    path(
        'trainingBlocks/topico/list/',
        views.trainingblockstopico_list,
        name='trainingblockstopico_list'
    ),
    path(
        'trainingBlocks/topico/<int:pk>/',
        views.trainingblockstopico_detail,
        name='trainingblockstopico_detail'
    ),
    path(
        'trainingBlocks/topico/<int:pk>/edit/',
        views.trainingblockstopico_edit,
        name='trainingblockstopico_edit'
    ),
    path(
        'trainingBlocks/topico/<int:pk>/delete/',
        views.trainingblockstopico_delete,
        name='trainingblockstopico_delete'
    ),

    # URLs Training Blocks
    path(
        'trainingBlocks/new/',
        views.trainingblocks_new,
        name='trainingblocks_new'
    ),
    path(
        'trainingBlocks/list/',
        views.trainingblocks_list,
        name='trainingblocks_list'
    ),
    path(
        'trainingBlocks/<int:pk>/',
        views.trainingblocks_detail,
        name='trainingblocks_detail'
    ),
    path(
        'trainingBlocks/<int:pk>/edit/',
         views.trainingblocks_edit,
         name='trainingblocks_edit'
    ),
    path(
        'trainingBlocks/<int:pk>/delete/',
        views.trainingblocks_delete,
        name='trainingblocks_delete'
    ),
]

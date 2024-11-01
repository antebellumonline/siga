# apps/centroProva/urls.py

"""
Definição das URLs para o aplicativo 'centroProva'.

Ele mapeia as requisições HTTP para as respectivas views, 
permitindo a navegação e interação com o sistema.
"""

from django.urls import path
from . import views

urlpatterns = [
    #URL página Principal do Centro de Provas
    path('centroProva/', views.centroProva_home, name='centroProva_home'),

    # URLs Centro de Provas
    path('centroProva/new/', views.centroProva_new, name='centroProva_new'),
    path('centroProva/list/', views.centroProva_list, name='centroProva_list'),
    path('centroProva/<int:pk>/', views.centroProva_detail, name='centroProva_detail'),
    path('centroProva/<int:pk>/edit/', views.centroProva_edit, name='centroProva_edit'),
    path('centroProva/<int:pk>/delete/', views.centroProva_delete, name='centroProva_delete'),

    # URLs Exames Realizados
    path('centroProva/exame/new/', views.exame_new, name='exame_new'),
    path('centroProva/exame/list/', views.exame_list, name='exame_list'),
    path('centroProva/exame/<int:pk>/', views.exame_detail, name='exame_detail'),
    path('centroProva/exame/<int:pk>/edit/', views.exame_edit, name='exame_edit'),
    path('centroProva/exame/<int:pk>/delete/', views.exame_delete, name='exame_delete'),
]

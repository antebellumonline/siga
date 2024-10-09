from django.urls import path
from . import views

urlpatterns = [
    #URL página Principal do Centro de Provas
    path('centroProva/', views.centroProva_home, name='centroProva_home'),

    # URLs Centro de Provas
    path('centroProva/new/', views.centroProva_new, name='centroProva_new'),
    path('centroProva/<int:pk>/', views.centroProva_detail, name='centroProva_detail'),
    path('centroProva/<int:pk>/edit/', views.centroProva_edit, name='centroProva_edit'),
    path('centroProva/<int:pk>/delete/', views.centroProva_delete, name='centroProva_delete'),
    path('centroProva/list/', views.centroProva_list, name='centroProva_list'),
    path('centroProva/reports/', views.centroProva_reports, name='centroProva_reports'),

    # URLs Exames Realizados
    path('centroProva/exame/new/', views.exame_new, name='exame_new'),
    path('centroProva/exame/list/', views.exame_list, name='exame_list'),
    path('centroProva/exame/reports/', views.exame_reports, name='exame_reports'),
]
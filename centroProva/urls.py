from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # URLs Centro de Provas
    path('centro_prova/novo/', views.centro_prova_novo, name='centro_prova_novo'),
    path('centro_prova/localizar/', views.centro_prova_localizar, name='centro_prova_localizar'),
    path('centro_prova/relatorios/', views.centro_prova_relatorios, name='centro_prova_relatorios'),
    
    # URLs Exames Realizados
    path('exame/novo/', views.exame_novo, name='exame_novo'),
    path('exame/localizar/', views.exame_localizar, name='exame_localizar'),
    path('exame/relatorios/', views.exame_relatorios, name='exame_relatorios'),
]
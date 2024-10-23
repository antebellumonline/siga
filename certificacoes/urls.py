from django.urls import path
from . import views

urlpatterns = [
    # URL da Página Inicial das Certificações
    path('certificacao/', views.certificacao_home, name='certificacao_home'),

    # URLS Certificadores
    path('certificador/list/', views.certificador_list, name='certificador_list'),
    path('certificador/<int:pk>/', views.certificador_detail, name='certificador_detail'),
    path('certificador/<int:pk>/edit/', views.certificador_edit, name='certificador_edit'),
    path('certificador/new/', views.certificador_new, name='certificador_new'),  # Sem mudanças aqui
    path('certificador/<int:pk>/delete/', views.certificador_delete, name='certificador_delete'),

    # URLS Certificações
    path('certificacao/new/', views.certificacao_new, name='certificacao_new'),  # Sem mudanças aqui
    path('certificacao/list/', views.certificacao_list, name='certificacao_list'),
    path('certificacao/<str:pk>/', views.certificacao_detail, name='certificacao_detail'),  # Alterado para <int:pk>
    path('certificacao/<str:pk>/edit/', views.certificacao_edit, name='certificacao_edit'),  # Alterado para <int:pk>
    path('certificacao/<str:pk>/delete/', views.certificacao_delete, name='certificacao_delete'),  # Alterado para <int:pk>
]

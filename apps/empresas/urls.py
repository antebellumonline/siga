# apps/empresas/urls.py

"""
Definição das URLs para o aplicativo 'empresas'.
"""

from django.urls import path
from . import views

# URLs Empresas
urlpatterns = [
    path('empresa/', views.empresa_home, name='empresa_home'),
    path('empresa/new/', views.empresa_new, name='empresa_new'),
    path('empresa/list/', views.empresa_list, name='empresa_list'),
    path('empresa/<str:pk>/', views.empresa_detail, name='empresa_detail'),
    path('empresa/<str:pk>/edit/', views.empresa_edit, name='empresa_edit'),
    path('empresa/<str:pk>/delete/', views.empresa_delete, name='empresa_delete'),
]

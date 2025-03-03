# apps/instrutores/urls.py

"""
Definição das URLs para o aplicativo 'instrutores'.
"""

from django.urls import path
from . import views

# URLs Instrutores
urlpatterns = [
    path('instrutor/', views.instrutor_home, name='instrutor_home'),
    path('instrutor/new/', views.instrutor_new, name='instrutor_new'),
    path('instrutor/list/', views.instrutor_list, name='instrutor_list'),
    path('instrutor/<str:pk>/', views.instrutor_detail, name='instrutor_detail'),
    path('instrutor/<str:pk>/edit/', views.instrutor_edit, name='instrutor_edit'),
        path('instrutor/<str:pk>/delete/', views.instrutor_delete, name='instrutor_delete'),
]

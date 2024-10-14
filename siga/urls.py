"""
URLs do projeto siga.

Este módulo configura as URLs para o projeto siga, incluindo as URLs do aplicativo alunos
e as URLs para login e logout.
"""

from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import delete_item

urlpatterns = [
    # Path para a interface Administrativa
    path('admin/', admin.site.urls),
    # Inclui as URLs do app 'alunos'
    path('', include('alunos.urls')),
    # Inclui as URLs do app 'certificacoes'
    path('', include('certificacoes.urls')),
    # Inclui as URLs do app 'centroProva'
    path('', include('centroProva.urls')),
    # Path para o logout do usuário
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Path para eclusão de registros
    path('delete/<str:model_name>/<int:pk>/', delete_item, name='delete_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

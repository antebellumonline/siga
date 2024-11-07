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
from .views import delete_item, home, buscar_endereco

urlpatterns = [
    # URL para a interface Administrativa Django
    path('admin/', admin.site.urls),

    # URL para a Página Inicial do Projeto
    path('', home, name='home'),

    # URLs de Login e Logout do Usuário
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # URLs dos apps
    path('', include('alunos.urls')),
    path('', include('certificacoes.urls')),
    path('', include('centroProva.urls')),

    # Path para eclusão de registros
    path('delete/<str:model_name>/<int:pk>/', delete_item, name='delete_item'),

    # Path para buscar endereço
    path('buscar-endereco/', buscar_endereco, name='buscar_endereco'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

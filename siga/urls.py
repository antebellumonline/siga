# siga/urls.py

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
from django.views.generic import RedirectView
from .views import delete_item, home, clientes

urlpatterns = [
    # URL para a interface Administrativa Django
    path('admin/', admin.site.urls),

    # URL para a Página Inicial do Projeto
    path('', home, name='home'),

    # URLs de Login e Logout do Usuário
    path('accounts/', include('allauth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # URLs para Recuperação de Senha
    path(
        'recuperar-senha/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset.html'
        ),
        name='password_reset'
    ),
    path(
        'recuperar-senha/sucesso/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/sucesso/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    # URL para a página de clientes
    path('clientes/', clientes, name='clientes'),

    # URL para a documentação do projeto
    path('docs/', RedirectView.as_view(url='/static/index.html')),

    # URLs dos apps
    path('apis/', include('apis.urls')),
    path('', include('apps.alunos.urls')),
    path('', include('apps.certificacoes.urls')),
    path('', include('apps.centroProva.urls')),
    path('', include('apps.cursos.urls')),
    path('', include('apps.empresas.urls')),
    path('', include('apps.instrutores.urls')),
    # path('', include('apps.turmas.urls')),

    # Path para exclusão de registros
    path('delete/<str:model_name>/<int:pk>/', delete_item, name='delete_item'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

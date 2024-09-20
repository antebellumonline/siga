# siga/urls.py (ou o nome do seu projeto)
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('alunos.urls')),  # Inclui as URLs do app alunos
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # URL para logout
]

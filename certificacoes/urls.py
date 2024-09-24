from django.urls import path
from .views import (
    certificador_list, certificador_detail, certificador_create,
    certificador_update, certificador_delete, 
    certificacao_list, certificacao_detail, certificacao_create,
    certificacao_update, certificacao_delete
)

urlpatterns = [
    path('certificadores/', certificador_list, name='certificador_list'),
    path('certificadores/<int:pk>/', certificador_detail, name='certificador_detail'),
    path('certificadores/create/', certificador_create, name='certificador_create'),
    path('certificadores/<int:pk>/update/', certificador_update, name='certificador_update'),
    path('certificadores/<int:pk>/delete/', certificador_delete, name='certificador_delete'),
    
    path('certificacoes/', certificacao_list, name='certificacao_list'),
    path('certificacoes/<int:pk>/', certificacao_detail, name='certificacao_detail'),
    path('certificacoes/create/', certificacao_create, name='certificacao_create'),
    path('certificacoes/<int:pk>/update/', certificacao_update, name='certificacao_update'),
    path('certificacoes/<int:pk>/delete/', certificacao_delete, name='certificacao_delete'),
]

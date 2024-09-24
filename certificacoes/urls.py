from django.urls import path
from .views import (
    certificador_list,
    certificador_detail,
    certificador_create,
    certificador_update,
    certificador_delete,
    certificacao_home,
    certificacao_list,
    certificacao_detail,
    certificacao_create,
    certificacao_update,
    certificacao_delete
)

urlpatterns = [
    # Rotas para certificadores
    path('certificador/list/', certificador_list, name='certificador_list'),
    path('certificador/<int:pk>/', certificador_detail, name='certificador_detail'),
    path('certificador/create/', certificador_create, name='certificador_create'),
    path('certificador/<int:pk>/update/', certificador_update, name='certificador_update'),
    path('certificador/<int:pk>/delete/', certificador_delete, name='certificador_delete'),
    
    # Rotas para certificações
    path('certificacao/', certificacao_home, name='certificacao_home'),
    path('certificacao/list/', certificacao_list, name='certificacao_list'),
    path('certificacao/<int:pk>/', certificacao_detail, name='certificacao_detail'),
    path('certificacao/create/', certificacao_create, name='certificacao_create'),
    path('certificacao/<str:pk>/update/', certificacao_update, name='certificacao_update'),
    path('certificacao/<str:pk>/delete/', certificacao_delete, name='certificacao_delete'),
]

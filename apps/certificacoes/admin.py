# apps/certificacoes/admin.py

"""
Configuração da interface administrativa para o app 'certificacoes'.

Ele registra os modelos para que possam ser gerenciados através do painel administrativo do Django,
definindo quais campos serão exibidos, quais podem ser pesquisados, 
filtrados e quais são somente leitura.
"""

from django.contrib import admin
from .models import Certificador, Certificacao

admin.site.register(Certificador)
admin.site.register(Certificacao)

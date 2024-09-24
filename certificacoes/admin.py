# certificacoes_app/admin.py

from django.contrib import admin
from .models import Certificador, Certificacao

admin.site.register(Certificador)
admin.site.register(Certificacao)

# apps/cursos/views.py

"""
Definição das views para o aplicativo 'centroProva'.

As views utilizam Django para gerenciar as requisições HTTP 
e interagir com os modelos de dados.
"""
from django.shortcuts import render

from .models import Curso, CursoCategoria

# ----- View para a Página Inicial do App Cursos -----
def curso_home(request):
    """
    View para a Página Inicial do App Cursos
    """
    return render(request, 'cursos/curso_home.html')

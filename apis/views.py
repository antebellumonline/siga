# apps/apis/views.py

"""
Definição das views para o aplicativo 'apis'.

As views utilizam Django para gerenciar as requisições HTTP 
e interagir com os modelos de dados.
"""

from django.http import JsonResponse
from .utils import busca_cep
import logging

logger = logging.getLogger(__name__)

def busca_cep(request, cep):
    try:
        dados = busca_cep(cep)
        if dados:
            return JsonResponse(dados)
        return JsonResponse({'resultado': '0'}, status=404)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=500)

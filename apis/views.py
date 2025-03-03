# apis/views.py

"""
Definição das views para o aplicativo 'apis'.

As views utilizam Django para gerenciar as requisições HTTP 
e interagir com os modelos de dados.
"""

import logging
from django.http import JsonResponse
from .utils import busca_cep as busca_cep_util
from .utils import busca_cnpj as busca_cnpj_util

logger = logging.getLogger(__name__)

def busca_cep_view(request, cep):
    """
    View para buscar informações de um CEP.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        cep (str): O CEP a ser buscado.

    Returns:
        JsonResponse: Dados do CEP ou mensagem de erro.
    """
    logger.info(
        "Requisição recebida de %s para buscar o CEP: %s",
        request.META.get('REMOTE_ADDR'), cep
    )
    try:
        dados = busca_cep_util(cep)
        if dados:
            if 'erro' in dados:
                return JsonResponse({'erro': dados['erro']}, status=400)
            return JsonResponse(dados)
        return JsonResponse({'resultado': '0'}, status=404)
    except ValueError as e:
        logger.error("Erro de valor ao buscar CEP: %s", e)
        return JsonResponse({'erro': 'An internal error has occurred.'}, status=400)
    except KeyError as e:
        logger.error("Erro de chave ao buscar CEP: %s", e)
        return JsonResponse({'erro': 'An internal error has occurred.'}, status=400)
    except TypeError as e:
        logger.error("Erro de tipo ao buscar CEP: %s", e)
        return JsonResponse({'erro': 'An internal error has occurred.'}, status=400)
    except RuntimeError as e:
        logger.error("Erro de execução ao buscar CEP: %s", e)
        return JsonResponse({'erro': 'An internal error has occurred.'}, status=500)

def busca_cnpj_view(request, taxId):
    """
    View para buscar informações de um CNPJ.

    Args:
        request (HttpRequest): O objeto de requisição HTTP.
        taxId (str): O CNPJ a ser buscado.

    Returns:
        JsonResponse: Dados do CNPJ ou mensagem de erro.
    """
    logger.info(
        "Requisição recebida de %s para buscar o CNPJ: %s",
        request.META.get('REMOTE_ADDR'), taxId
    )
    try:
        dados = busca_cnpj_util(taxId)
        if dados:
            if 'erro' in dados:
                return JsonResponse({'erro': dados['erro']}, status=400)
            return JsonResponse(dados)
        return JsonResponse({'resultado': '0'}, status=404)
    except ValueError as e:
        logger.error("Erro de valor ao buscar CNPJ: %s", e)
        return JsonResponse({'erro': 'An internal error has occurred.'}, status=400)
    except KeyError as e:
        logger.error("Erro de chave ao buscar CNPJ: %s", e)
        return JsonResponse({'erro': 'An internal error has occurred.'}, status=400)
    except TypeError as e:
        logger.error("Erro de tipo ao buscar CNPJ: %s", e)
        return JsonResponse({'erro': 'An internal error has occurred.'}, status=400)
    except RuntimeError as e:
        logger.error("Erro de execução ao buscar CNPJ: %s", e)
        return JsonResponse({'erro': 'An internal error has occurred.'}, status=500)

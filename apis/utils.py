# apis/utils.py

"""
Este módulo contém funções utilitárias para a implementação de APIs.
"""

import logging
import requests

# Configuração do logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def busca_cep(cep):
    """
    Busca informações de um CEP usando a BrasilAPI e complementa com dados do IBGE.

    Args:
        cep (str): O CEP a ser buscado.

    Returns:
        dict: Um dicionário contendo informações do CEP, ou None se não encontrado.
    """
    url_brasilapi = f"https://brasilapi.com.br/api/cep/v1/{cep}"
    try:
        response_brasilapi = requests.get(url_brasilapi, timeout=10)
        if response_brasilapi.status_code == 200:
            data = response_brasilapi.json()
            cidade = data.get("city")
            uf = data.get("state")
            if cidade and uf:
                url_ibge = (
                    f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
                    f"?nome={cidade}&uf={uf}"
                )
                response_ibge = requests.get(url_ibge, timeout=10)
                if response_ibge.status_code == 200:
                    municipios = response_ibge.json()
                    for municipio in municipios:
                        if (
                            municipio["nome"].lower() == cidade.lower() and
                            municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"] == uf
                        ):
                            data["ibge"] = municipio["id"]
                            break
                return {
                    "cep": data.get("cep"),
                    "logradouro": data.get("street"),
                    "complemento": data.get("complement"),
                    "bairro": data.get("neighborhood"),
                    "cidade": data.get("city"),
                    "uf": data.get("state"),
                    "ibge": data.get("ibge")
                }
    except requests.exceptions.RequestException as e:
        logger.error("Erro ao buscar CEP: %s", e)
        return {"erro": "Erro ao buscar informações do CEP"}
    return None

def busca_cnpj(cnpj):
    """
    Busca informações de um CNPJ usando a API BrasilAPI.

    Args:
        cnpj (str): O CNPJ a ser buscado.

    Returns:
        dict: Um dicionário contendo informações do CNPJ, ou None se não encontrado.
    """
    url_brasil_api = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"

    try:
        response = requests.get(url_brasil_api, timeout=10)
        logger.info("Status da resposta da API BrasilAPI: %s", response.status_code)

        if response.status_code == 200:
            data = response.json()
            logger.info("Dados recebidos da API BrasilAPI: %s", data)

            if 'erro' in data:
                logger.error("Erro na resposta da API BrasilAPI: %s", data['erro'])
                return None

            cidade = data.get("municipio")
            uf = data.get("uf")
            descricao_tipo_de_logradouro = data.get("descricao_tipo_de_logradouro", "")
            logradouro = data.get("logradouro", "")

            # Concatenando logradouro com descricao_tipo_de_logradouro
            endereco_completo = f"{descricao_tipo_de_logradouro} {logradouro}".strip()

            if cidade and uf:
                url_ibge = (
                    f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios"
                    f"?nome={cidade}&uf={uf}"
                )
                response_ibge = requests.get(url_ibge, timeout=10)
                if response_ibge.status_code == 200:
                    municipios = response_ibge.json()
                    for municipio in municipios:
                        if (
                            municipio["nome"].lower() == cidade.lower() and
                            municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"] == uf
                        ):
                            data["ibge"] = municipio["id"]
                            break

            if cidade and uf:
                return {
                    "taxID": data.get("cnpj"),
                    "razaoSocial": data.get("razao_social"),
                    "fantasia": data.get("nome_fantasia"),
                    "cep": data.get("cep"),
                    "endereco": endereco_completo,
                    "numero": data.get("numero"),
                    "complemento": data.get("complemento"),
                    "bairro": data.get("bairro"),
                    "cidade": data.get("municipio"),
                    "uf": data.get("uf"),
                    "ibge": data.get("ibge")
                }
        else:
            logger.error("Erro na resposta da API BrasilAPI. Status code: %s", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        logger.error("Erro ao buscar CNPJ: %s", e)
        return {"erro": "Erro ao buscar informações do CNPJ"}
    return None

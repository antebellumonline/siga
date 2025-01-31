# apis/utils.py

"""
Este módulo contém funções utilitárias para a implementação de APIs.
"""

import requests

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

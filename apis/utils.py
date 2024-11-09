# apis/utils.py

import requests

import requests

def busca_cep(cep):
    url_brasilapi = f"https://brasilapi.com.br/api/cep/v1/{cep}"
    try:
        response_brasilapi = requests.get(url_brasilapi, timeout=10)
        if response_brasilapi.status_code == 200:
            data = response_brasilapi.json()
            cidade = data.get("city")
            uf = data.get("state")
            if cidade and uf:
                url_ibge = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios?nome={cidade}&uf={uf}"
                response_ibge = requests.get(url_ibge, timeout=10)
                if response_ibge.status_code == 200:
                    municipios = response_ibge.json()
                    for municipio in municipios:
                        if municipio["nome"].lower() == cidade.lower() and municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"] == uf:
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
        return {"erro": str(e)}
    return None

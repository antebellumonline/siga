# apps/apis/utils.py

import requests

def busca_cep(cep):
    url = f"http://republicavirtual.com.br/web_cep.php?cep={cep}&formato=json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# apps/apis/views.py

"""
Definição das views para o aplicativo 'apis'.

As views utilizam Django para gerenciar as requisições HTTP 
e interagir com os modelos de dados.
"""

import requests
from django.shortcuts import render
from .forms import EnderecoForm

def busca_cep(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST)
        if form.is_valid():
            cep = form.cleaned_data['cep']
            response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
            data = response.json()
            form = EnderecoForm(initial={
                'cep': cep,
                'logradouro': data.get('logradouro', ''),
                'bairro': data.get('bairro', ''),
                'cidade': data.get('localidade', ''),
                'estado': data.get('uf', ''),
            })
    else:
        form = EnderecoForm()
    return render(request, 'busca_cep.html', {'form': form})
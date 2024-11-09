# cidades/forms.py

"""
Este módulo contém os formulários utilizados para o aplicativo cidades.
Ele define os formulários para cadastro, edição e outras operações relacionadas aos Endereços.
"""

from django import forms
from cidades.models import Endereco

class EnderecoForm(forms.Form):
    cep = forms.CharField(label='CEP', max_length=8)
    logradouro = forms.CharField(label='Logradouro', max_length=255, required=False)
    bairro = forms.CharField(label='Bairro', max_length=100, required=False)
    cidade = forms.CharField(label='Cidade', max_length=100, required=False)
    estado = forms.CharField(label='Estado', max_length=2, required=False)

    def buscar_cep(self):
        cep = self.cleaned_data.get('cep')
        if cep:
            try:
                endereco = Endereco.objects.get(cep=cep)
                self.cleaned_data['logradouro'] = endereco.logradouro
                self.cleaned_data['bairro'] = endereco.bairro
                self.cleaned_data['cidade'] = endereco.cidade.nome
                self.cleaned_data['estado'] = endereco.cidade.estado.uf
            except Endereco.DoesNotExist:
                self.add_error('cep', 'CEP não encontrado.')

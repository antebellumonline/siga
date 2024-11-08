# apps/apis/forms.py

"""
Este módulo contém os formulários utilizados para o aplicativo 'apis'.
Ele define os formulários para cadastro, edição e outras operações relacionadas aos Alunos.
"""

from django import forms

class EnderecoForm(forms.Form):
    cep = forms.CharField(label='CEP', max_length=8)
    logradouro = forms.CharField(label='Logradouro', max_length=100, required=False)
    bairro = forms.CharField(label='Bairro', max_length=100, required=False)
    cidade = forms.CharField(label='Cidade', max_length=100, required=False)
    estado = forms.CharField(label='Estado', max_length=2, required=False)

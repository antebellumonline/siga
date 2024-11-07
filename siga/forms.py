# siga/forms.py

from django import forms
import requests
from cidades.models import Cidade

class EnderecoForm(forms.Form):
    cep = forms.CharField(max_length=9, required=True)
    logradouro = forms.CharField(max_length=100, required=False)
    bairro = forms.CharField(max_length=100, required=False)
    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), required=False)

    def clean_cep(self):
        cep = self.cleaned_data.get('cep')
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        if response.status_code == 200:
            data = response.json()
            if "erro" not in data:
                self.cleaned_data['logradouro'] = data.get('logradouro', '')
                self.cleaned_data['bairro'] = data.get('bairro', '')
                cidade_nome = data.get('localidade', '')
                uf = data.get('uf', '')
                try:
                    cidade = Cidade.objects.get(nome=cidade_nome, estado__uf=uf)
                    self.cleaned_data['cidade'] = cidade
                except Cidade.DoesNotExist:
                    raise forms.ValidationError("Cidade não encontrada no banco de dados.")
            else:
                raise forms.ValidationError("CEP não encontrado.")
        else:
            raise forms.ValidationError("Erro ao buscar o CEP.")
        return cep

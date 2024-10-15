from django import forms
from .models import Certificacao, Certificador

class CertificadorForm(forms.ModelForm):
    class Meta:
        model = Certificador
        fields = ['descricao', 'siglaCertificador', 'inativo']

class CertificacaoForm(forms.ModelForm): 
    class Meta:
        model = Certificacao
        fields = ['idCertificador', 'descricao', 'siglaExame', 'duracao', 'observacao', 'inativo']

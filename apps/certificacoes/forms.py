# apps/certificacoes/forms.py

"""
Este módulo contém os formulários utilizados para o aplicativo de Certificações.
Ele define os formulários para cadastro, edição e outras operações relacionadas às Certificações.
"""

from django import forms
from .models import Certificacao, Certificador

class CertificadorForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Certificadores.

    Este formulário é baseado no modelo Aluno e define os campos que serão exibidos no formulário, 
    além de customizar a aparência dos campos utilizando widgets.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = Certificador
        fields = ['descricao', 'siglaCertificador', 'inativo']

class CertificacaoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Certificações.

    Este formulário é baseado no modelo Aluno e define os campos que serão exibidos no formulário, 
    além de customizar a aparência dos campos utilizando widgets.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = Certificacao
        fields = ['idCertificador', 'descricao', 'siglaExame', 'duracao', 'observacao', 'inativo']

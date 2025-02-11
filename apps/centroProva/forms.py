# apps/centroProva/forms.py

"""
Este módulo contém os formulários utilizados para o aplicativo Centro de Provas.
Ele define os formulários para cadastro, edição e outras operações relacionadas ao Centro de Provas.
"""

from django import forms
from .models import CentroProva, CentroProvaExame

class CentroProvaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Centros de Provas.

    Este formulário é baseado no modelo CentroProva e define os campos
    que serão exibidos no formulário
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = CentroProva
        fields = [
            'nome',
            'inativo'
        ]

class CentroProvaExameForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Exames Realizados Centros de Provas.

    Este formulário é baseado no modelo CentroProvaExane e define os campos
    que serão exibidos no formulário, além de customizar a aparência dos campos utilizando widgets.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = CentroProvaExame
        fields = [
            'certificacao',
            'centroProva',
            'aluno',
            'data',
            'presenca',
            'cancelado',
            'observacao'
        ]
        widgets = {
            'data': forms.DateTimeInput(attrs={
                'id': 'edit-select-dataExame',
                'type': 'datetime-local',
                'placeholder': 'Selecione a data e hora do exame'
            }),
        }

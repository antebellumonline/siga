# apps/centroProva/forms.py

"""
Este módulo contém os formulários utilizados para o aplicativo Centro de Provas.
"""

from django import forms

from apps.alunos.models import Aluno
from apps.certificacoes.models import Certificacao
from apps.auxiliares.widgets import BooleanSelect

from .models import CentroProva, CentroProvaExame
class CentroProvaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Centros de Provas.
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
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'centroProva-nome',
                'name': 'centroProva-nome',
                'label': 'Nome do Centro de Provas: ',
                'placeholder': 'Informe o nome do Centro de Prova',
                'autofocus': True,
            }),
            'inativo': BooleanSelect(attrs={
                'class': 'apps-form-input select2',
                'id': 'centroProva-inativo',
                'name': 'centroProva-inativo',
                'label': 'Status: ',
                'placeholder': 'Selecione o status do Centro de Prova',
            }),
        }

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
            'data',
            'centroProva',
            'certificacao',
            'aluno',
            'presenca',
            'cancelado',
            'observacao'
        ]
        widgets = {
            'data': forms.DateTimeInput(attrs={
                'class': 'apps-form-input',
                'id': 'exame-data',
                'name': 'exame-data',
                'type': 'datetime-local',
                'label': 'Data e Hora do Exame: ',
                'placeholder': 'Selecione a data e hora do Exame',
                'autofocus': True,
            }),
            'centroProva': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'exame-centroProva',
                'name': 'exame-centroProva',
                'label': 'Centro de Provas: ',
                'placeholder': 'Selecione o Centro de Provas',
            }),
            'certificacao': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'exame-certificacao',
                'name': 'exame-certificacao',
                'label': 'Certificação: ',
                'placeholder': 'Selecione a Certificação',
            }),
            'aluno': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'exame-aluno',
                'name': 'exame-aluno',
                'label': 'Aluno: ',
                'placeholder': 'Selecione o Aluno',
            }),
            'presenca': BooleanSelect(attrs={
                'class': 'apps-form-input select2',
                'id': 'exame-presenca',
                'name': 'exame-presenca',
                'label': 'Presença: ',
                'placeholder': 'Marque se o aluno compareceu ao exame',
            }),
            'cancelado': BooleanSelect(attrs={
                'class': 'apps-form-input select2',
                'id': 'exame-cancelado',
                'name': 'exame-cancelado',
                'label': 'Cancelado: ',
                'placeholder': 'Marque se o exame foi cancelado',
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'apps-form-input',
                'id': 'exame-observacao',
                'name': 'exame-observacao',
                'label': 'Observação: ',
                'placeholder': 'Digite uma observação sobre o exame',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['data'].initial = self.instance.data.strftime('%Y-%m-%dT%H:%M')

        self.fields['certificacao'].queryset = (
            Certificacao.objects
            .filter(inativo=False)
            .order_by('descricao')
        )
        self.fields['certificacao'].label_from_instance = self.certificacao_label_from_instance
        self.fields['aluno'].queryset = (
            Aluno.objects
            .filter(inativo=False)
            .order_by('nome')
        )
        self.fields['aluno'].label_from_instance = self.aluno_label_from_instance

    def certificacao_label_from_instance(self, obj):
        """
        Gera uma string de rótulo para uma instância de certificação.
        """
        return f"{obj.descricao} ({obj.siglaExame})"

    def aluno_label_from_instance(self, obj):
        """
        Gera uma string de rótulo para uma instância de certificação.
        """
        return f"{obj.uid} - {obj.nome}"

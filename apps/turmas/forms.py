# apps/turmas/forms.py

"""
Este módulo contém os formulários utilizados para o App Turmas.
"""

from django import forms

from apps.auxiliares.widgets import BooleanSelect

from .models import Turma

class TurmaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Turmas.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = Turma
        fields = [
            'curso',
            'versaoCurso',
            'tipo',
            'empresa',
            'local',
            'nome',
            'inicioCurso',
            'terminoCurso',
            'datasCurso',
            'enturmacao',
            'plataforma',
            'material',
            'certificado',
            'observacao',
            'inativo'
        ]
        widgets = {
            'curso': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-curso',
                'name': 'turma-curso',
                'label': 'Curso: ',
                'placeholder': 'Selecione o Curso',
                'autofocus': True,
            }),
            'versaoCurso': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-versaoCurso',
                'name': 'turma-versaoCurso',
                'label': 'Versão do Curso: ',
                'placeholder': 'Selecione a Versão do Curso',
            }),
            'tipo': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-tipo',
                'name': 'turma-tipo',
                'label': 'Tipo de Turma: ',
                'placeholder': 'Selecione o Tipo de Turma',
                'autofocus': True,
            }),
            'empresa': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-empresa',
                'name': 'turma-empresa',
                'label': 'Empresa: ',
                'placeholder': 'Selecione a Empresa',
            }),
            'local': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-local',
                'name': 'turma-local',
                'label': 'Local: ',
                'placeholder': 'Selecione o Local',
            }),
            'nome': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-nome',
                'name': 'turma-nome',
                'label': 'Nome da Turma: ',
                'placeholder': 'Digite o Nome da Turma',
            }),
            'inicioCurso': forms.DateTimeInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-inicioCurso',
                'name': 'turma-inicioCurso',
                'type': 'datetime-local',
                'label': 'Data e Hora de Início do Curso: ',
                'placeholder': 'Digite a Data de Início do Curso',
            }),
            'terminoCurso': forms.DateTimeInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-terminoCurso',
                'name': 'turma-terminoCurso',
                'type': 'datetime-local',
                'label': 'Data e Hora de Término do Curso: ',
                'placeholder': 'Digite a Data de Término do Curso',
            }),
            'datasCurso': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-datasCurso',
                'label': 'Datas do Curso: ',
                'name': 'turma-datasCurso',
                'placeholder': 'Digite as Datas do Curso',
            }),
            'enturmacao': BooleanSelect(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-enturmacao',
                'name': 'turma-enturmacao',
                'label': 'Alunos Enturmados? ',
            }),
            'plataforma': BooleanSelect(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-plataforma',
                'name': 'turma-plataforma',
                'label': 'A Turma está na Plataforma? ',
            }),
            'material': BooleanSelect(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-material',
                'name': 'turma-material',
                'label': 'O Material foi Dispobilizado? ',
            }),
            'certificado': BooleanSelect(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-certificado',
                'name': 'turma-certificado',
                'label': 'O Certificado de Participação foi emitido? ',
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'apps-form-input',
                'id': 'turma-observacao',
                'name': 'turma-observacao',
                'placeholder': 'Digite as Observações sobre a Turma',
                'rows': 4,
            }),
            'inativo': BooleanSelect(attrs={
                'class': 'apps-form-input inativo-input select2',
                'id': 'turma-inativo',
                'name': 'turma-inativo',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            if self.instance.inicioCurso:
                self.fields['inicioCurso'].initial = self.instance.inicioCurso.strftime('%Y-%m-%dT%H:%M')
            if self.instance.terminoCurso:
                self.fields['terminoCurso'].initial = self.instance.terminoCurso.strftime('%Y-%m-%dT%H:%M')

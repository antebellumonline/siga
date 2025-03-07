# apps/turmas/forms.py

"""
Este módulo contém os formulários utilizados para o App Turmas.
"""

from django import forms

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
                'placeholder': 'Selecione o Curso',
                'autofocus': True,
            }),
            'versaoCurso': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-versaoCurso',
                'name': 'turma-versaoCurso',
                'placeholder': 'Selecione a Versão do Curso',
            }),
            'tipo': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-tipo',
                'name': 'turma-tipo',
                'placeholder': 'Selecione o Tipo de Turma',
            }),
            'empresa': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-empresa',
                'name': 'turma-empresa',
                'placeholder': 'Selecione a Empresa',
            }),
            'local': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'turma-local',
                'name': 'turma-local',
                'placeholder': 'Selecione o Local',
            }),
            'nome': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-nome',
                'name': 'turma-nome',
                'placeholder': 'Digite o Nome da Turma',
            }),
            'inicioCurso': forms.DateTimeInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-inicioCurso',
                'name': 'turma-inicioCurso',
                'placeholder': 'Digite a Data de Início do Curso',
            }),
            'terminoCurso': forms.DateTimeInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-terminoCurso',
                'name': 'turma-terminoCurso',
                'placeholder': 'Digite a Data de Término do Curso',
            }),
            'datasCurso': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-datasCurso',
                'name': 'turma-datasCurso',
                'placeholder': 'Digite as Datas do Curso',
            }),
            'enturmacao': forms.CheckboxInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-enturmacao',
                'name': 'turma-enturmacao',
            }),
            'plataforma': forms.CheckboxInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-plataforma',
                'name': 'turma-plataforma',
            }),
            'material': forms.CheckboxInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-material',
                'name': 'turma-material',
            }),
            'certificado': forms.CheckboxInput(attrs={
                'class': 'apps-form-input',
                'id': 'turma-certificado',
                'name': 'turma-certificado',
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'apps-form-input',
                'id': 'turma-observacao',
                'name': 'turma-observacao',
                'placeholder': 'Digite uma Observação sobre a Turma',
                'rows': 4,
            }),
            'inativo': forms.CheckboxInput(attrs={
                'class': 'apps-form-input inativo-input',
                'id': 'turma-inativo',
                'name': 'turma-inativo',
            }),
        }

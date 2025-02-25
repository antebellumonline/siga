# apps/cursos/forms.py

"""
Este módulo contém os formulários utilizados para o App Cursos.
Ele define os formulários para cadastro, edição e outras operações relacionadas aos Cursos.
"""
from django import forms
from django.forms import inlineformset_factory

from apps.certificacoes.models import Certificacao
from .models import (
    Curso,
    CursoCategoria,
    CursoCertificacao,
    TrainingBlocksTopico,
    TrainingBlocks,
    CursoTrainingBlocks
)

class CursoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Cursos.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = Curso
        fields = ['nome', 'categoria', 'codigo', 'inativo']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'inativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CursoCategoriaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Categorias de Cursos.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = CursoCategoria
        fields = [
            'nome',
            'sigla',
            'inativo'
        ]

class CursoCertificacaoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Relacionamento
    entre Cursos e Certificações.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = CursoCertificacao
        fields = [
            'id',
            'certificacao',
        ]
        widgets = {
            'curso': forms.Select(attrs={'class': 'form-control'}),
            'certificacao': forms.Select(attrs={'class': 'form-control select2'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['certificacao'].queryset = Certificacao.objects.filter(inativo=False).order_by('descricao')
        self.fields['certificacao'].label_from_instance = self.certificacao_label_from_instance

    def certificacao_label_from_instance(self, obj):
        return f"{obj.descricao} ({obj.siglaExame})"

CursoCertificacaoFormSet = inlineformset_factory(
    Curso,
    CursoCertificacao,
    form=CursoCertificacaoForm,
    extra=4,
    can_delete=True
)

class TrainingBlocksTopicoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Tópicos da Training Blocks.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = TrainingBlocksTopico
        fields = [
            'nome',
            'codigo',
            'inativo'
        ]

class TrainingBlocksForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Training Blocks.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = TrainingBlocks
        fields = ['codigo',
                  'topico',
                  'duracao',
                  'descricao',
                  'observacao',
                  'inativo'
            ]
        widgets = {
            'topico': forms.Select(attrs={'class': 'form-control'}),
            'duracao': forms.DateInput(attrs={'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'inativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CursoTrainingBlocksForm (forms.ModelForm):
    """
    Formulário para cadastro e edição de Relacionamento
    entre Cursos e Training Blocks.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = CursoTrainingBlocks
        fields = [
            'curso',
            'trainingBlocks',
            'topico',
            'ordem',
            'observacao',
            'inativo'
        ]
        widgets = {
            'curso': forms.Select(attrs={'class': 'form-control select2'}),
            'trainingBlocks': forms.Select(attrs={'class': 'form-control select2'}),
            'topico': forms.Select(attrs={'class': 'form-control select2'}),
            'ordem': forms.TextInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['curso'].queryset = Curso.objects.all().order_by('codigo')
        self.fields['curso'].label_from_instance = self.curso_label_from_instance

    def curso_label_from_instance(self, obj):
        return f"{obj.codigo}: {obj.nome}"

CursoTrainingBlocksFormSet = inlineformset_factory(
    TrainingBlocks,
    CursoTrainingBlocks,
    form=CursoTrainingBlocksForm,
    extra=4,
    can_delete=True
)

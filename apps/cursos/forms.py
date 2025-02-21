# apps/cursos/forms.py

"""
Este módulo contém os formulários utilizados para o App Cursos.
Ele define os formulários para cadastro, edição e outras operações relacionadas aos Cursos.
"""
from django import forms
from django.forms import inlineformset_factory
from .models import Curso, CursoCategoria, CursoCertificacao, TrainingBlocksTopico
from apps.certificacoes.models import Certificacao

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'categoria', 'codigo', 'inativo']
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'inativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CursoCategoriaForm(forms.ModelForm):
    class Meta:
        model = CursoCategoria
        fields = ['nome', 'sigla', 'inativo']

class CursoCertificacaoForm(forms.ModelForm):
    class Meta:
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
    class Meta:
        model = TrainingBlocksTopico
        fields = ['nome', 'inativo']

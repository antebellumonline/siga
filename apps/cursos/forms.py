# apps/cursos/forms.py

"""
Este módulo contém os formulários utilizados para o App Cursos.
Ele define os formulários para cadastro, edição e outras operações relacionadas aos Cursos.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Curso, CursoCategoria, CursoCertificacao

class CursoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Cursos.

    Este formulário é baseado no modelo Curso e define os campos que serão exibidos no formulário, 
    além de customizar a aparência dos campos utilizando widgets.
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

    Este formulário é baseado no modelo CursoCategoria e define os campos que serão exibidos no formulário, 
    além de customizar a aparência dos campos utilizando widgets.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = CursoCategoria
        fields = [
            'nome',
            'sigla', 'inativo'
        ]

class CursoCertificacaoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Certificações dos Cursos.

    Este formulário é baseado no modelo Cursos e define os campos que serão exibidos no formulário, 
    além de customizar a aparência dos campos utilizando widgets.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = CursoCertificacao
        fields = [
            'curso',
            'certificacao'
        ]

        widgets = {
            'curso': forms.HiddenInput(),
            'certificacao': forms.Select(attrs={'class': 'form-control'})
        }

# FormSet para Certificações dos Cursos
CursoCertificacaoFormSet = inlineformset_factory(
    Curso,
    CursoCertificacao,
    form=CursoCertificacaoForm,
    extra=0,
    can_delete=True
)

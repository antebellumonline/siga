# apps/alunos/forms.py

"""
Este módulo contém os formulários utilizados para o aplicativo de alunos.
Ele define os formulários para cadastro, edição e outras operações relacionadas aos alunos.
"""

from django import forms
from .models import Aluno, AlunoContato

class AlunoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de alunos.

    Este formulário é baseado no modelo Aluno e define os campos que serão exibidos no formulário, 
    além de customizar a aparência dos campos utilizando widgets.
    """

    class Meta:
        """
        Configurações meta do formulário.
        """
        model = Aluno # Modelo relacionado ao formulário
        fields = [
            'uid', 
            'nome', 
            'cpf', 
            'cep', 
            'endereco', 
            'numero', 
            'complemento', 
            'bairro', 
            'cidade', 
            'observacao', 
            'inativo'
            ]
        widgets = {
            'cidade': forms.Select(attrs={'class': 'form-control'}),  # Dropdown de cidade
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
            'observacao': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'inativo': forms.CheckboxInput()
        }

class AlunoContatoForm(forms.ModelForm):
    class Meta:
        model = AlunoContato
        fields = [
            'tipoContato',
            'contato',
            'detalhe']
        widgets = {
            'tipoContato': forms.Select(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'detalhe': forms.Textarea(attrs={'class': 'form-control'}),
        }
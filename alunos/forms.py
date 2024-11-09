# alunos/forms.py

"""
Este módulo contém os formulários utilizados para o aplicativo de Alunos.
Ele define os formulários para cadastro, edição e outras operações relacionadas aos Alunos.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Aluno, AlunoContato, ConfigTpContato

class AlunoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Alunos.

    Este formulário é baseado no modelo Aluno e define os campos que serão exibidos no formulário, 
    além de customizar a aparência dos campos utilizando widgets.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = Aluno
        fields = [
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
            'cidade': forms.Select(attrs={'class': 'form-control', 'id': 'cidade', 'name': 'cidade'}),
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP', 'id': 'cep', 'name': 'cep'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'id': 'logradouro', 'name': 'logradouro'}),
            'numero': forms.TextInput(attrs={'class': 'form-control', 'id': 'numero', 'name': 'numero'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'id': 'complemento', 'name': 'complemento'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'id': 'bairro', 'name': 'bairro'}),
            'observacao': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'inativo': forms.CheckboxInput()
        }

class AlunoContatoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de contatos de alunos.

    Este formulário é baseado no modelo AlunoContato e define os campos necessários para
    adicionar ou atualizar informações de contato do aluno, utilizando widgets personalizados.
    """
    class Meta:
        """
        Configurações meta do formulário AlunoContatoForm.
        """
        model = AlunoContato
        fields = [
            'id',
            'tipoContato',
            'contato',
            'detalhe'
        ]
        widgets = {
            'aluno': forms.Select(attrs={'class': 'form-control'}),
            'tipoContato': forms.Select(attrs={'class': 'form-control select2'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'detalhe': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipoContato'].queryset = ConfigTpContato.objects.order_by('descricao')

# FormSet para contatos do aluno
AlunoContatoFormSet = inlineformset_factory(
    Aluno,
    AlunoContato,
    form=AlunoContatoForm,
    extra=4,
    can_delete=True
)

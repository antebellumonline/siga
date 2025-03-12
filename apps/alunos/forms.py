# apps/alunos/forms.py

"""
Este módulo contém os formulários utilizados para o aplicativo de Alunos.
Ele define os formulários para cadastro, edição e outras operações relacionadas aos Alunos.
"""

from django import forms
from django.forms import inlineformset_factory
from .models import Aluno, AlunoContato, ConfigTpContato, Cidade

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
            'nome': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'aluno-nome',
                'name': 'aluno-nome',
                'placeholder': 'Digite o Nome do Aluno',
            }),
            'cpf': forms.TextInput(attrs={
                'class': 'apps-form-input cpf-mask',
                'id': 'aluno-cpf',
                'name': 'aluno-cpf',
                'placeholder': 'Digite o CPF do Aluno',
            }),
            'cep': forms.TextInput(attrs={
                'class': 'apps-form-input cep-input cep-mask',
                'id': 'aluno-cep',
                'name': 'aluno-cep',
                'placeholder': 'Digite o CEP do Aluno',
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'apps-form-input logradouro-input',
                'id': 'aluno-logradouro',
                'name': 'aluno-logradouro',
                'placeholder': 'Digite o Endereço do Aluno',
            }),
            'numero': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'aluno-numero',
                'name': 'aluno-numero',
                'placeholder': 'Digite o Número do Endereço',
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'aluno-complemento',
                'name': 'aluno-complemento',
                'placeholder': 'Digite o Complemento do Endereço',
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'apps-form-input bairro-input',
                'id': 'aluno-bairro',
                'name': 'aluno-bairro',
                'placeholder': 'Digite o Bairro do Aluno',
            }),
            'cidade': forms.Select(attrs={
                'class': 'apps-form-input cidade-input select2',
                'id': 'aluno-cidade',
                'name': 'aluno-cidade',
                'placeholder': 'Selecione a Cidade do Aluno',
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'apps-form-input',
                'id': 'aluno-observacao',
                'name': 'aluno-observacao',
                'placeholder': 'Digite uma Observação sobre o Aluno',
                'rows': 4,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cidade'].queryset = Cidade.objects.select_related('estado').order_by('nome')
        self.fields['cidade'].label_from_instance = self.cidade_label_from_instance

    def cidade_label_from_instance(self, obj):
        """
        Retorna uma string formatada com o nome da Cidade e o Estado.
        """
        return f"{obj.nome} / {obj.estado.uf}"
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
            'empresa': forms.Select(attrs={
                'class': 'apps-form-input',
                'id': 'alunoContato-aluno',
                'name': 'alunoContato-aluno',
                'placeholder': 'Selecione o Aluno',
            }),
            'tipoContato': forms.Select(attrs={
                'class': 'apps-form-input select2 tipo-contato',
                'id': 'alunoContato-tipoContato',
                'name': 'alunoContato-tipoContato',
                'placeholder': 'Selecione o Tipo de Contato',
            }),
            'contato': forms.TextInput(attrs={
                'class': 'apps-form-input contato-mask',
                'id': 'alunoContato-contato',
                'name': 'alunoContato-contato',
                'placeholder': 'Digite o Contato',
            }),
            'detalhe': forms.Textarea(attrs={
                'class': 'apps-form-input',
                'id': 'alunoContato-detalhe',
                'name': 'alunoContato-detalhe',
                'placeholder': 'Digite algum detalhe sobre o Contato',
                'rows': 2,
            }),
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

# apps/empresas/forms.py

"""
Este módulo contém os formulários utilizados para o App Cursos.
"""

from django import forms
from django.forms import inlineformset_factory

from .models import Empresa, EmpresaContato, Cidade, ConfigTpContato

class EmpresaForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Empresas.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = Empresa
        fields = [
            'taxId',
            'razaoSocial',
            'fantasia',
            'endereco',
            'numero',
            'complemento',
            'bairro',
            'cep',
            'cidade',
            'observacao',
            'inativo'
        ]
        widgets = {
            'taxId': forms.TextInput(attrs={
                'class': 'apps-form-input taxId-input',
                'id': 'empresa-taxId',
                'name': 'empresa-taxId',
                'placeholder': 'Digite o CNPJ ou Tax ID da Empresa',
            }),
            'razaoSocial': forms.TextInput(attrs={
                'class': 'apps-form-input razaoSocial-input',
                'id': 'empresa-razaoSocial',
                'name': 'empresa-razaoSocial',
                'placeholder': 'Digite a Razão Social da Empresa',
            }),
            'fantasia': forms.TextInput(attrs={
                'class': 'apps-form-input fantasia-input',
                'id': 'empresa-fantasia',
                'name': 'empresa-fantasia',
                'placeholder': 'Digite o Nome Fantasia da Empresa',
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'apps-form-input logradouro-input',
                'id': 'empresa-logradouro',
                'name': 'empresa-logradouro',
                'placeholder': 'Digite o Endereço da Empresa',
            }),
            'numero': forms.TextInput(attrs={
                'class': 'apps-form-input endereco-numero-input',
                'id': 'empresa-numero',
                'name': 'empresa-numero',
                'placeholder': 'Digite o Número do Endereço',
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'apps-form-input complemento-input',
                'id': 'empresa-complemento',
                'name': 'empresa-complemento',
                'placeholder': 'Digite o Complemento do Endereço',
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'apps-form-input bairro-input',
                'id': 'empresa-bairro',
                'name': 'empresa-bairro',
                'placeholder': 'Digite o Bairro da Empresa',
            }),
            'cep': forms.TextInput(attrs={
                'class': 'apps-form-input cep-input cep-mask',
                'id': 'empresa-cep',
                'name': 'empresa-cep',
                'placeholder': 'Digite o CEP da Empresa',
            }),
            'cidade': forms.Select(attrs={
                'class': 'apps-form-input cidade-input select2',
                'id': 'empresa-cidade',
                'name': 'empresa-cidade',
                'placeholder': 'Digite a Cidade da Empresa',
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'apps-form-input',
                'id': 'empresa-observacao',
                'name': 'empresa-observacao',
                'placeholder': 'Digite alguma observação sobre a Empresa',
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

class EmpresaContatoForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de contatos das Empresas.
    """
    class Meta:
        """
        Configurações meta do formulário.
        """
        model = EmpresaContato
        fields = [
            'empresa',
            'tipoContato',
            'contato',
            'detalhe'
        ]
        widgets = {
            'empresa': forms.Select(attrs={
                'class': 'apps-form-input',
                'id': 'empresaContato-empresa',
                'name': 'empresaContato-empresa',
                'placeholder': 'Selecione a Empresa',
            }),
            'tipoContato': forms.Select(attrs={
                'class': 'apps-form-input select2',
                'id': 'empresaContato-tipoContato',
                'name': 'empresaContato-tipoContato',
                'placeholder': 'Selecione o Tipo de Contato',
            }),
            'contato': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'empresaContato-contato',
                'name': 'empresaContato-contato',
                'placeholder': 'Digite o Contato',
            }),
            'detalhe': forms.Textarea(attrs={
                'class': 'apps-form-input',
                'id': 'empresaContato-detalhe',
                'name': 'empresaContato-detalhe',
                'placeholder': 'Digite algum detalhe sobre o Contato',
                'rows': 2,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipoContato'].queryset = ConfigTpContato.objects.order_by('descricao')

# FormSet para contatos das Empresas
EmpresaContatoFormSet = inlineformset_factory(
    Empresa,
    EmpresaContato,
    form=EmpresaContatoForm,
    extra=1,
    can_delete=True,
)

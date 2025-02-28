# apps/instrutores/forms.py

"""
Este módulo contém os formulários utilizados para o aplicativo 'instrutores'.
Ele define os formulários para cadastro, edição e outras operações relacionadas aos Instrutores.
"""

from django import forms
from .models import Instrutor

class InstrutorForm(forms.ModelForm):
    """
    Formulário para cadastro e edição de Centros de Provas.

    """
    class Meta:
        """Configurações meta do formulário"""
        model = Instrutor
        fields = [
            'nome',
            'observacao',
            'inativo',
        ]
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'apps-form-input',
                'id': 'instrutor-nome',
                'placeholder': 'Digite o nome do Instrutor',
            }),
            'observacao': forms.Textarea(attrs={
                'class': 'apps-form-input',
                'id': 'instrutor-observacao',
                'placeholder': 'Escreva alguma observação sobre o Instrutor',
                'rows': 2,
            }),
            'inativo': forms.CheckboxInput(attrs={
                'class': 'apps-form-input',
                'id': 'instrutor-inativo',
            }),
        }

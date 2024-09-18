# apps/alunos/forms.py
from django import forms
from .models import Aluno

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'cpf', 'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'observacao', 'inativo']
        widgets = {
            'observacao': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'inativo': forms.CheckboxInput()
        }
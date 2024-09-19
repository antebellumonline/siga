# apps/alunos/forms.py
from django import forms
from .models import Aluno
from localidades.models import Cidade  # Certifique-se de que o modelo Cidade está importado

class AlunoForm(forms.ModelForm):
    cidade = forms.ModelChoiceField(queryset=Cidade.objects.all(), widget=forms.Select, required=True)
    class Meta:
        model = Aluno
        fields = ['uid', 'nome', 'cpf', 'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'observacao', 'inativo']
        widgets = {
            'cidade': forms.Select(attrs={'class': 'form-control'}),  # Dropdown de cidade
            'cep': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CEP'}),
            'observacao': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'inativo': forms.CheckboxInput()
        }
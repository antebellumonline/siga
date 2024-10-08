from django import forms
from .models import CentroProva, CentroProvaExame

class CentroProvaForm(forms.ModelForm):
    class Meta:
        model = CentroProva
        fields = ['nome', 'inativo']

class CentroProvaExameForm(forms.ModelForm):
    class Meta:
        model = CentroProvaExame
        fields = ['certificacao', 'centroProva', 'aluno', 'data', 'presenca', 'cancelado', 'observacao']

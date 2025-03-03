# apps/auxiliares/fields.py

"""
Este módulo contém definições de campos personalizados para o projeto.
"""

from django.db import models

class InativoField(models.BooleanField):
    """
    Um campo BooleanField personalizado que utiliza escolhas
    específicas para indicar se algo está inativo.
    """
    def __init__(self, *args, **kwargs):
        inativo_choices = [
            (False, 'Não'),
            (True, 'Sim'),
        ]
        kwargs['choices'] = inativo_choices
        super().__init__(*args, **kwargs)

# apps/auxiliares/fields.py

from django.db import models

class InativoField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        inativo_choices = [
            (False, 'Não'),
            (True, 'Sim'),
        ]
        kwargs['choices'] = inativo_choices
        super().__init__(*args, **kwargs)

from django.db import models

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    codigo_ibge = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.nome} ({self.codigo_ibge})'

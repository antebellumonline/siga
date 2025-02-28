# apps/instrutores/models.py

"""
Definições dos modelos do aplicativo 'instrutores'.

Este arquivo contém as classes de modelos usadas para representar e manipular
os dados relacionados aos Instrutores no banco de dados.
"""

from django.db import models
from apps.auxiliares.fields import InativoField

class Instrutor(models.Model):
    """
    Modelo que representa um Instrutor no sistema.
    """
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    observacao = models.TextField(blank=True, null=True)
    inativo = InativoField(default=False)

    def __str__(self):
        return str(self.nome)

    class Meta:
        """Meta-informações para o modelo Instrutor"""
        db_table = 'tb_instrutor'

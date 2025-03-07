# apps/local/models.py

"""
Definições dos modelos do aplicativo 'local'.
"""

from django.db import models

class Estado(models.Model) :
    """
    Modelo que representa um Estado no sistema.
    """
    id = models.CharField(primary_key=True, max_length=2, unique=True)
    nome = models.CharField(max_length=255)
    uf = models.CharField(max_length=2, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.id}, {self.nome}'

    class Meta:
        """Meta-informações para o modelo Estado."""
        db_table = 'tb_uf'

class Cidade(models.Model):
    """
    Modelo que representa uma Cidade no sistema.
    """
    id = models.CharField(primary_key=True, max_length=7, unique=True)
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.nome} ({self.id})'

    class Meta:
        """Meta-informações para o modelo Cidade."""
        db_table = 'tb_uf-cidade'

class Local (models.Model):
    """
    Modelo que representa um local.
    """
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nome)

    class Meta:
        """Meta-informações para o modelo Local"""
        db_table = 'tb_local'

# apps/empresas/models.py

"""
Definições dos modelos do aplicativo 'empresas'.

Este arquivo contém as classes de modelos usadas para representar e manipular
os dados relacionados aos alunos no banco de dados.
"""

from django.db import models
from apps.local.models import Cidade
from apps.auxiliares.models import ConfigTpContato
from apps.auxiliares.fields import InativoField

class Empresa(models.Model):
    """
    Modelo que representa um Curso.
    """
    id = models.AutoField(primary_key=True)
    taxId = models.CharField(max_length=255, unique=True)
    razaoSocial = models.CharField(max_length=255)
    fantasia = models.CharField(max_length=255)
    cep = models.CharField(max_length=8, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, blank=True, null=True)
    observacao = models.TextField(null=True, blank=True)
    inativo = InativoField()

    def __str__(self):
        return self.razaoSocial

    class Meta:
        """Meta-informações para o modelo Empresa."""
        db_table = 'tb_empresa'

class EmpresaContato(models.Model):
    """
    Modelo que representa os Contatos de uma Empresa.
    """
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='contatos')
    tipoContato = models.ForeignKey(ConfigTpContato, on_delete=models.CASCADE)
    contato = models.CharField(max_length=255)
    detalhe = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        """
        Retorna uma string com o tipo de contato e o contato.
        """
        # pylint: disable=no-member
        return f'Contato de {self.empresa.razaoSocial}: {self.tipoContato.descricao}'

    class Meta:
        """Meta-informações para o modelo EmpresaContato."""
        db_table = 'tb_empresa-contato'

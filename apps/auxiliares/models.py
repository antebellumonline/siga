# apps/auxiliares/models.py

"""
Definições dos modelos do aplicativo 'auxiliares'.
"""

from django.db import models

class ConfigTpContato(models.Model):
    """
    Modelo que representa os Tipos de Contato.
    """
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255, unique=True)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.descricao)

    class Meta:
        """Meta-informações para o modelo ConfigTpContato."""
        db_table = 'tb_config-tpContato'

class ConfigStatus(models.Model):
    """
    Modelo que representa os Status.
    """
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nome)

    class Meta:
        """Meta-informações para o modelo Instrutor"""
        db_table = 'tb_configStatus'

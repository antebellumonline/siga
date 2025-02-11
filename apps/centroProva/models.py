# apps/centroProva/models.py

"""
Definições dos modelos do aplicativo 'centroProva'.

Este arquivo contém as classes de modelos usadas para representar e manipular
os dados relacionados aos alunos no banco de dados.
"""
from datetime import datetime

from django.db import models
from apps.certificacoes.models import Certificacao
from apps.alunos.models import Aluno

class CentroProva(models.Model):
    """Modelo que representa um Centro de Provas."""

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nome)

    class Meta:
        """Meta-informações para o modelo CentroProva."""
        db_table = 'tb_centroProva'

class CentroProvaExame(models.Model):
    """Modelo que representa um Exame Realizado no Centro de Prova."""

    id = models.AutoField(primary_key=True)
    certificacao = models.ForeignKey(Certificacao, on_delete=models.PROTECT)
    centroProva = models.ForeignKey(CentroProva, on_delete=models.PROTECT)
    aluno = models.ForeignKey(Aluno, on_delete=models.PROTECT)
    data = models.DateTimeField()
    presenca = models.BooleanField(default=False)
    cancelado = models.BooleanField(default=False)
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        if isinstance(self.data, datetime):
            formatted_date = self.data.strftime('%d/%m/%Y %H:%M:%S')
        else:
            formatted_date = 'Data não definida'

        return f"{self.certificacao} - {self.centroProva} - {self.aluno} - {formatted_date}"

    class Meta:
        """Meta-informações para o modelo CentroProvaExame."""
        db_table = 'tb_centroProva-exames'
        unique_together = ('aluno', 'data')

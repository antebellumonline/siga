# apps/cursos/models.py

"""
Definições dos modelos do aplicativo 'centroProva'.

Este arquivo contém as classes de modelos usadas para representar e manipular
os dados relacionados aos alunos no banco de dados.
"""

import re

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from apps.certificacoes.models import Certificacao

def validate_codigo(value):
    """
    Valida se o código da categoria do curso está no formato correto.
    """
    if not re.match(r'^\d{1,3}\.\d{2}$', value):
        raise ValidationError(
            'Código deve estar no formato #.#0, com até três dígitos antes e dois depois do ponto.'
        )

class CursoCategoria(models.Model):
    """
    Modelo que representa uma Categoria de Curso.
    """

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    sigla = models.CharField(max_length=3, unique=True)
    inativo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que a sigla seja salva em caixa alta.
        """
        if self.sigla:
            self.sigla = self.sigla.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.nome)

    class Meta:
        """Meta-informações para o modelo CursoCategoria."""
        db_table = 'tb_curso-categoria'

class Curso(models.Model):
    """
    Modelo que representa um Curso.
    """

    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=6)
    nome = models.CharField(max_length=255)
    categoria = models.ForeignKey(CursoCategoria, on_delete=models.PROTECT)
    inativo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que o Código seja salvo em caixa alta.
        """
        if self.codigo:
            self.codigo = self.codigo.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.nome)

    class Meta:
        """Meta-informações para o modelo Curso."""
        db_table = 'tb_curso'

class CursoVersao(models.Model):
    """
    Modelo que representa as Versões de um Curso.
    """

    id = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    versao = models.CharField(
        max_length=6,
        validators = [
            RegexValidator(
                regex=r'^\d+\.\d+$',
                message=(
                    'A versão deve ser um número no formato X.Y, '
                    'por exemplo: 2.1, 30.5, 30.57, etc.'
                )
            )
        ]
    )
    codigo = models.CharField(max_length=255)
    cargaHoraria = models.DurationField(default='00:00:00')
    nome = models.CharField(max_length=255)

    def __str__(self):
        return str(self.versao)

    class Meta:
        """Meta-informações para o modelo Curso."""
        db_table = 'tb_curso-versao'

class CursoCertificacao(models.Model):
    """
    Modelo que representa a relação entre Curso e Certificação.
    """
    id = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='certificacoes')
    certificacao = models.ForeignKey(Certificacao, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.curso} - {self.certificacao}"

    class Meta:
        """Meta-informações para o modelo CursoCertificacao."""
        db_table = 'tb_curso-certificacao'
        unique_together = ('curso', 'certificacao')

class TrainingBlocksTopico(models.Model):
    """Modelo que representa um Tópico de Bloco de Treinamento."""

    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=7, validators=[validate_codigo])
    nome = models.CharField(max_length=255)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nome)

    class Meta:
        """Meta-informações para o modelo trainingBlocksTopico."""
        db_table = 'tb_trainingBlocks-topico'
        ordering = [models.functions.Cast('codigo', output_field=models.FloatField())]

class TrainingBlocks(models.Model):
    """Modelo que representa um Bloco de Treinamento."""

    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=7, validators=[validate_codigo])
    duracao = models.DurationField(default='00:00:00')
    descricao = models.CharField(max_length=255)
    topico = models.ForeignKey(
        TrainingBlocksTopico,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
        )
    gravado = models.BooleanField(default=False)
    observacao = models.TextField(blank=True, null=True)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.descricao)

    class Meta:
        """Meta-informações para o modelo TrainingBlocks."""
        db_table = 'tb_trainingBlocks'
        ordering = [models.functions.Cast('codigo', output_field=models.FloatField())]

class CursoTrainingBlocks(models.Model):
    """Modelo que representa a relação entre Curso e Training Blocks."""

    id = models.AutoField(primary_key=True)
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='cursos'
    )
    trainingBlocks = models.ForeignKey(
        TrainingBlocks,
        on_delete=models.CASCADE,
        related_name='trainingblocks'
    )
    topico = models.ForeignKey(
        TrainingBlocksTopico,
        on_delete=models.CASCADE,
        related_name='topico'
    )
    ordem = models.CharField(max_length=7, validators=[validate_codigo])
    observacao = models.TextField(blank=True, null=True)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.curso} - {self.trainingBlocks} - {self.ordem}"

    class Meta:
        """Meta-informações para o modelo CursoTrainingBlocks."""
        db_table = 'tb_curso-trainingBlocks'
        unique_together = ('curso', 'trainingBlocks', 'ordem')
        ordering = [models.functions.Cast('ordem', output_field=models.FloatField())]

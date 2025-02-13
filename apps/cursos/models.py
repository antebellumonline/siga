# apps/cursos/models.py

"""
Definições dos modelos do aplicativo 'centroProva'.

Este arquivo contém as classes de modelos usadas para representar e manipular
os dados relacionados aos alunos no banco de dados.
"""

from django.db import models
from apps.certificacoes.models import Certificacao

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

    id = models.CharField(max_length=6, primary_key=True)
    codigo = models.CharField(max_length=3)
    nome = models.CharField(max_length=255)
    categoria = models.ForeignKey(CursoCategoria, on_delete=models.SET_NULL, blank=True, null=True)
    cargaHoraria = models.PositiveIntegerField()
    inativo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id and self.categoria and self.codigo:
            self.id = f"{self.categoria.sigla}{self.codigo}"
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.nome)

    class Meta:
        """Meta-informações para o modelo Curso."""
        db_table = 'tb_curso'

class CursoCertificacao(models.Model):
    """
    Modelo que representa a relação entre Curso e Certificação.
    """
    id = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
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
    nome = models.CharField(max_length=255)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nome)

    class Meta:
        """Meta-informações para o modelo trainingBlocksTopico."""
        db_table = 'tb_trainingBlocks-topico'

class TrainingBlocks(models.Model):
    """Modelo que representa um Bloco de Treinamento."""

    id = models.CharField(max_length=10, primary_key=True)
    duracao = models.DurationField(default='00:00:00')
    descricao = models.CharField(max_length=255)
    topico = models.ForeignKey(
        TrainingBlocksTopico,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
        )
    obsevacao = models.TextField(blank=True, null=True)
    inativo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id and self.topico:
            # Gerar o ID no formato correto
            ultimo_id = TrainingBlocks.objects.filter(topico=self.topico).count() + 1
            self.id = f"{self.topico.id}.{ultimo_id:02d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.descricao)

    class Meta:
        """Meta-informações para o modelo TrainingBlocks."""
        db_table = 'tb_trainingBlocks'

class CursoTrainingBlocks(models.Model):
    """Modelo que representa a relação entre Curso e Bloco de Treinamento."""

    id = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    trainingBlocks = models.ForeignKey(TrainingBlocks, on_delete=models.CASCADE)
    topico = models.ForeignKey(TrainingBlocksTopico, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField()
    observacao = models.TextField(blank=True, null=True)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.curso} - {self.trainingBlocks} - {self.ordem}"

    class Meta:
        """Meta-informações para o modelo CursoTrainingBlocks."""
        db_table = 'tb_curso-trainingBlocks'
        unique_together = ('curso', 'trainingBlocks', 'ordem')

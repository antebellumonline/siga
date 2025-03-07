# apps/turmas/models.py

"""
Definições dos modelos do aplicativo 'centroProva'.
"""

from django.db import models
from apps.cursos.models import Curso, CursoVersao
from apps.empresas.models import Empresa
from apps.local.models import Local

class TipoTurma (models.Model):
    """Modelo que representa um Tipo de Turma."""
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return str(self.nome)

    class Meta:
        """Meta-informações para o modelo TipoTurma"""
        db_table = 'tb_tipoTurma'

class Turma (models.Model):
    """Modelo que representa uma Turma."""
    id = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    versaoCurso = models.ForeignKey(CursoVersao, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoTurma, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=3, unique=True)
    inicioCurso = models.DateTimeField(blank=True, null=True)
    terminoCurso = models.DateTimeField(blank=True, null=True)
    datasCurso = models.CharField(max_length=255, blank=True, null=True)
    enturmacao = models.BooleanField(default=False)
    plataforma = models.BooleanField(default=False)
    material = models.BooleanField(default=False)
    certificado = models.BooleanField(default=False)
    observacao = models.TextField(blank=True, null=True)
    inativo = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para garantir que o Código seja salvo em caixa alta.
        """
        if self.codigo:
            self.codigo = self.codigo.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.codigo)

    class Meta:
        """Meta-informações para o modelo Turma"""
        db_table = 'tb_turma'

from django.db import models
from certificacoes.models import Certificacao
from alunos.models import Aluno

class CentroProva(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = 'tb_centroProva'
    
class CentroProvaExame(models.Model):
    id = models.AutoField(primary_key=True)
    certificacao = models.ForeignKey(Certificacao, on_delete=models.CASCADE) # Referencia a tabela tb_certificacao
    centroProva = models.ForeignKey(CentroProva, on_delete=models.CASCADE) # Referencia a tabela tb_centroProva
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE) # Referencia a tabela tb_aluno
    data = models.DateTimeField() # Data e hora do exame
    presenca = models.BooleanField(default=False) # Campo booleano: True para presente, False para ausente
    cancelado = models.BooleanField(default=False) # Campo booleano: True para cancelado, False para não cancelado
    observacao = models.TextField(blank=True, null=True)  # Observações sobre o Centro de Provas
    def __str__(self):
        return f"{self.certificacao} - {self.centro_prova} - {self.aluno}"
    
    class Meta:
        db_table = 'tb_centroProva-exames'

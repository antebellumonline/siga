# certificacoes_app/models.py

from django.db import models

class Certificador(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao
    
    class Meta:
        db_table = 'tb_certificador'

class Certificacao(models.Model):
    id = models.AutoField(primary_key=True)
    certificador = models.ForeignKey(Certificador, on_delete=models.CASCADE)
    descricao = models.TextField()
    sigla_exame = models.CharField(max_length=50)
    duracao = models.CharField(max_length=50)  # Ajuste o tipo conforme a necessidade
    observacao = models.TextField(blank=True, null=True)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao
    
    class Meta:
        db_table = 'tb_certificacao'

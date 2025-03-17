# apps/dfs/models.py

"""
Definições dos modelos do aplicativo 'turmas'.
"""

from datetime import datetime
from django.db import models
from apps.auxiliares.models import ConfigStatus
from apps.alunos.models import Aluno
from apps.empresas.models import Empresa

class NfseEmit (models.Model):
    """Modelo que representa uma Nota Fiscal de Serviços Emitida."""
    id = models.AutoField(primary_key=True)
    cv = models.CharField(max_length=10)
    chaveAcesso = models.CharField(max_length=50, blank=True, null=True)
    numero = models.CharField(max_length=10)
    status = models.ForeignKey(ConfigStatus, on_delete=models.PROTECT)
    emissao = models.DateTimeField
    competencia = models.CharField(max_length=8)
    cliente = models.CharField(max_length=255)
    servico = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=28, decimal_places=2)
    issqn = models.DecimalField(max_digits=28, decimal_places=2)
    pis = models.DecimalField(max_digits=28, decimal_places=2)
    cofins = models.DecimalField(max_digits=28, decimal_places=2)
    csll = models.DecimalField(max_digits=28, decimal_places=2)
    ir = models.DecimalField(max_digits=28, decimal_places=2)
    inss = models.DecimalField(max_digits=28, decimal_places=2)
    desconto = models.DecimalField(max_digits=28, decimal_places=2)
    valor_total = models.DecimalField(
        max_digits=28,
        decimal_places=2,
        blank=True,
        null=True,
        default=0,
        db_column='valorTotal'
    )

    def busca_cliente(self):
        """Busca e define o cliente com base no CPF ou Tax ID."""
        aluno = Aluno.objects.filter(cpf=self.cv).first()
        empresa = Empresa.objects.filter(taxId=self.cv).first()

        if aluno and aluno.cpf:
            self.cliente = f"{aluno.nome} (Aluno)"
        elif empresa and empresa.taxId:
            self.cliente = f"{empresa.razaoSocial} (Empresa)"
        else:
            self.cliente = "Cliente não encontrado"

        self.save()

    def calcula_valor_total(self):
        """Calcula o valor total subtraindo impostos e descontos."""
        impostos_descontos = (self.issqn + self.pis + self.cofins +
                              self.csll + self.ir + self.inss + self.desconto
        )
        self.valor_total = self.valor - impostos_descontos

    def save(self, *args, **kwargs):
        self.busca_cliente()
        self.calcula_valor_total()
        super(NfseEmit, self).save(*args, **kwargs)

    def __str__(self):
        if isinstance(self.emissao, datetime):
            formatted_emissao = self.emissao.strftime('%d/%m/%Y %H:%M')
        else:
            formatted_emissao = 'Data de Emissão não definida'

        return f"{self.cv}: {formatted_emissao}"

    class Meta:
        """Meta-informações para o modelo NfseEmit"""
        db_table = 'tb_nfse-emit'

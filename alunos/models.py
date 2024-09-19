"""
Este módulo contém os modelos para o app de Alunos. 
Ele define as tabelas e relacionamentos no banco de dados.
"""

from django.db import models

class Cidade(models.Model):
    nome = models.CharField(max_length=100)
    codigo_ibge = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f'{self.nome} - {self.codigo_ibge}'

class Aluno(models.Model):
    """
    Modelo que representa um aluno no sistema.
    """
    uid = models.AutoField(primary_key=True)  # Código único
    nome = models.CharField(max_length=255)  # Nome completo do aluno
    cpf = models.CharField(max_length=11, blank=True, null=True)  # CPF do aluno
    cep = models.CharField(max_length=8, blank=True, null=True)  # CEP
    endereco = models.CharField(max_length=255, blank=True, null=True)  # Endereço
    numero = models.CharField(max_length=10, blank=True, null=True)  # Número da residência
    complemento = models.CharField(max_length=255, blank=True, null=True)  # Complemento (opcional)
    bairro = models.CharField(max_length=255, blank=True, null=True)  # Bairro
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)  # Código da cidade conforme IBGE
    observacao = models.TextField(blank=True, null=True)  # Observações sobre o aluno
    inativo = models.BooleanField(default=False)  # Status: 0 Ativo, 1 Inativo

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para definir o UID inicial. 
        Note que isso deve ser usado com cautela.
        """
        if self._state.adding and self.uid is None:
            last_id = Aluno.objects.aggregate(models.Max('uid'))['uid__max']
            if last_id is None:
                self.uid = 10000000
            else:
                self.uid = last_id + 1
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Retorna uma representação em string do objeto Aluno.
        Exibe o UID e o nome do aluno.
        """
        return f'Aluno {self.uid}; {self.nome}'

    class Meta:
        db_table = 'tb_aluno'


class ConfigTpContato(models.Model):
    """
    Modelo que representa os tipos de contato.
    Exemplo: Celular Pessoal, Telefone Corporativo, E-mail Pessoal.
    """
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255, unique=True)  # Exemplo: "Celular Pessoal", "E-mail Corporativo"
    inativo = models.BooleanField(default=False)  # Status: 0 Ativo, 1 Inativo

    def __str__(self):
        """
        Retorna a descrição do tipo de contato.
        """
        return f'{self.descricao} - {"Inativo" if self.inativo else "Ativo"}'

    class Meta:
        db_table = 'tb_config_tpContato'


class AlunoContato(models.Model):
    """
    Modelo que representa os contatos do aluno.
    """
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)  # Relaciona com a tabela Aluno
    tipo_contato = models.ForeignKey(ConfigTpContato, on_delete=models.CASCADE)  # Relaciona com a tabela ConfigTpContato
    contato = models.CharField(max_length=255)  # Celular, telefone ou e-mail
    detalhe = models.TextField(blank=True, null=True)  # Observações adicionais

    def __str__(self):
        """
        Retorna uma string com o tipo de contato e o contato.
        """
        return f'Contato de {self.aluno.nome}: {self.tipo_contato.descricao} - {self.contato}'

    class Meta:
        db_table = 'tb_aluno-contato'

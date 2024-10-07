"""
Este módulo contém os modelos para o app de Alunos. 
Ele define as tabelas e relacionamentos no banco de dados.
"""

from django.db import models
from cidades.models import Cidade

class Aluno(models.Model):
    """
    Modelo que representa um aluno no sistema.

    Cada aluno possui um ID único (uid), nome, CPF, endereço, cidade, entre outras informações.
    O campo 'uid' é gerado automaticamente e serve como chave primária.
    O campo 'cidade' é uma chave estrangeira para a tabela de cidades, 
    estabelecendo uma relação de um para muitos.
    """
    uid = models.AutoField(primary_key=True)  # Código único
    nome = models.CharField(max_length=255)  # Nome completo do aluno
    cpf = models.CharField(max_length=11, blank=True, null=True)  # CPF do aluno
    cep = models.CharField(max_length=8, blank=True, null=True)  # CEP
    endereco = models.CharField(max_length=255, blank=True, null=True)  # Endereço
    numero = models.CharField(max_length=10, blank=True, null=True)  # Número da residência
    complemento = models.CharField(max_length=255, blank=True, null=True)  # Complemento (opcional)
    bairro = models.CharField(max_length=255, blank=True, null=True)  # Bairro
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, blank=True, null=True)  # Código da cidade
    observacao = models.TextField(blank=True, null=True)  # Observações sobre o aluno
    inativo = models.BooleanField(default=False)  # Status: 0 Ativo, 1 Inativo

    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para definir o UID inicial 
        e garantir que o nome seja salvo em caixa alta.

        O UID é gerado automaticamente a partir do último ID utilizado, garantindo a unicidade.
        O nome é convertido para caixa alta para padronizar os dados.
        """

        # Garante que o nome seja salvo em caixa alta
        if self.nome:
            self.nome = self.nome.upper()

        # Lógica para definir o UID inicial
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
    Modelo que representa os tipos de contato possíveis para um aluno.

    Cada tipo de contato possui uma descrição única (ex: Celular Pessoal, E-mail Corporativo).
    """
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255, unique=True)  # Exemplo: "Celular Pessoal", "E-mail Corporativo"
    inativo = models.BooleanField(default=False)  # Status: 0 Ativo, 1 Inativo

    def __str__(self):
        """
        Retorna a descrição do tipo de contato.
        """
        return self.descricao

    class Meta:
        db_table = 'tb_config-tpContato'


class AlunoContato(models.Model):
    """
    Modelo que representa um contato específico de um aluno.

    Cada contato está relacionado a um aluno e a um tipo de contato.
    O relacionamento com Aluno é do tipo CASCADE, o que significa que se um aluno for deletado,
    seus contatos também serão.
    """
    id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='contatos')  # Relaciona com a tabela Aluno
    tipoContato = models.ForeignKey(ConfigTpContato, on_delete=models.CASCADE)  # Relaciona com a tabela ConfigTpContato
    contato = models.CharField(max_length=255)  # Celular, telefone ou e-mail
    detalhe = models.TextField(blank=True, null=True)  # Observações adicionais

    def __str__(self):
        """
        Retorna uma string com o tipo de contato e o contato.
        """
        return f'Contato de {self.aluno.nome}: {self.tipoContato.descricao} - {self.contato}'

    class Meta:
        db_table = 'tb_aluno-contato'

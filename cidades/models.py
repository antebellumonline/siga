from django.db import models

class Estado(models.Model) :
    id = models.CharField(primary_key=True, max_length=2, unique=True)
    nome = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.id}, {self.nome}'
    
    class Meta:
        db_table = 'tb_uf'

class Cidade(models.Model):
    id = models.CharField(primary_key=True, max_length=7, unique=True)
    nome = models.CharField(max_length=100)
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.nome} ({self.id})'

    class Meta:
        db_table = 'tb_ufcidade'

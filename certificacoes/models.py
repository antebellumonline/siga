from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Certificador(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    siglaCertificador = models.CharField(max_length=3)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'tb_certificador'


class Certificacao(models.Model):
    id = models.CharField(max_length=7, primary_key=True)
    idCertificador = models.ForeignKey(Certificador, on_delete=models.CASCADE)
    descricao = models.TextField()
    siglaExame = models.CharField(max_length=50)
    duracao = models.IntegerField()
    observacao = models.TextField(blank=True, null=True)
    inativo = models.BooleanField(default=False)

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = 'tb_certificacao'


@receiver(pre_save, sender=Certificacao)
def gerar_id_certificacao(sender, instance, **kwargs):
    # Lógica para gerar o ID da certificação
    if not instance.id:  # Se for um novo registro
        # Pegar a sigla do certificador
        sigla = instance.idCertificador.siglaCertificador  # Use 'instance' aqui

        # Contar quantas certificações já existem com essa sigla no ID
        last_certificacao = Certificacao.objects.filter(id__startswith=sigla).order_by('-id').first()

        if last_certificacao:
            # Incrementar o número sequencial
            last_number = int(last_certificacao.id[-4:])  # Pega os últimos 4 dígitos do ID
            new_number = last_number + 1
        else:
            # Se for a primeira certificação com essa sigla
            new_number = 1

        # Formatar o novo ID com o padrão 'XXX0000'
        instance.id = f'{sigla}{new_number:04d}'  # Use 'instance' aqui
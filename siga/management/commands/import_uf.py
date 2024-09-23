import requests
from django.core.management.base import BaseCommand
from cidades.models import Estado

class Command(BaseCommand):
    help = 'Importa estados do IBGE'

    def handle(self, *args, **kwargs):
        # URL da API que fornece os estados
        url = "https://servicodados.ibge.gov.br/api/v3/malhas/estados/"

        response = requests.get(url)
        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Erro ao acessar a API.'))
            return

        estados_data = response.json()

        for estado_data in estados_data:
            estado_id = estado_data['id']  # Código do estado
            nome_estado = estado_data['nome']  # Nome do estado

            estado, created = Estado.objects.get_or_create(id=estado_id, defaults={'nome': nome_estado})

            if created:
                self.stdout.write(self.style.SUCCESS(f'Estado {nome_estado} importado com sucesso.'))
            else:
                self.stdout.write(self.style.WARNING(f'O estado {nome_estado} já existe.'))


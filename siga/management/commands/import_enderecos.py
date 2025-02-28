import requests
import logging
import os
import django
import time
import csv
from django.core.management.base import BaseCommand

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siga.settings')
django.setup()

from apps.local.models import Estado, Cidade, Endereco

# Configuração do logging
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'import_enderecos-log.txt')
csv_file = os.path.join(log_dir, 'import_enderecos.csv')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Command(BaseCommand):
    help = 'Importa todos os endereços usando a API do ViaCEP'

    def handle(self, *args, **kwargs):
        try:
            addresses = self.fetch_all_addresses()
            
            # Gerar arquivo CSV
            self.generate_csv(addresses)
            
            # Informar que o arquivo foi gerado e perguntar se deseja importar os dados para a tabela
            print(f"Arquivo CSV gerado em {csv_file}")
            confirm = input("Deseja importar esses endereços para a tabela? (s/n): ")
            if confirm.lower() == 's':
                self.add_addresses_to_db(addresses)
                self.stdout.write(self.style.SUCCESS("Endereços importados com sucesso!"))
                logging.info('Endereços importados com sucesso!')
            else:
                self.stdout.write(self.style.WARNING("Operação cancelada."))
                logging.info('Operação cancelada.')
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao processar os CEPs: {e}'))
            logging.error(f'Erro ao processar os CEPs: {e}')

    def fetch_all_addresses(self):
        addresses = []
        # Iterar sobre todos os CEPs possíveis
        for i in range(1000000, 1000100):  # Intervalo de exemplo, ajuste conforme necessário
            cep = f"{i:08d}"
            retries = 3
            while retries > 0:
                try:
                    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/', timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        if 'erro' not in data:
                            address = {
                                'cep': cep,
                                'logradouro': data.get('logradouro', ''),
                                'bairro': data.get('bairro', ''),
                                'cidade_nome': data.get('localidade', ''),
                                'cidade_id': data.get('ibge', ''),  # Usando o código IBGE da cidade
                                'estado_id': data.get('uf', '')
                            }
                            addresses.append(address)
                            print(f"CEP {cep} processado com sucesso.")
                    break
                except requests.exceptions.RequestException as e:
                    retries -= 1
                    logging.warning(f"Erro ao buscar CEP {cep}: {e}. Tentativas restantes: {retries}")
                    time.sleep(5)  # Pausa de 5 segundos antes de tentar novamente
                    if retries == 0:
                        print(f"Falha ao processar o CEP {cep} após várias tentativas.")
        return addresses

    def generate_csv(self, addresses):
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['CEP', 'Logradouro', 'Bairro', 'Cidade Nome', 'Cidade ID', 'Estado ID'])
            for address in addresses:
                writer.writerow([address['cep'], address['logradouro'], address['bairro'], address['cidade_nome'], address['cidade_id'], address['estado_id']])
        print(f"Arquivo CSV gerado em {csv_file}")

    def add_addresses_to_db(self, addresses):
        for address in addresses:
            cidade_id = address['cidade_id']
            cidade_nome = address['cidade_nome']
            logradouro = address['logradouro']
            bairro = address['bairro']
            
            # Obter ou criar Cidade
            cidade, created = Cidade.objects.get_or_create(
                id=cidade_id,
                defaults={'nome': cidade_nome}
            )
            
            # Criar Endereco
            Endereco.objects.create(
                cep=address['cep'],
                logradouro=logradouro,
                bairro=bairro,
                cidade=cidade
            )

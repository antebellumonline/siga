import pandas as pd
from django.core.management.base import BaseCommand
from apps.cidades.models import Cidade, Estado
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import logging
import os

# Configuração do logging (modificação para salvar na pasta 'logs')
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'import_cidades-log.txt')

logging.basicConfig(
    filename=log_file,  # Nome do arquivo de log dentro da pasta 'logs'
    level=logging.INFO,  # Define o nível do log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Command(BaseCommand):
    help = 'Importa cidades de uma planilha Excel'

    def handle(self, *args, **kwargs):
        # Oculta a janela principal do Tkinter
        Tk().withdraw()
        
        # Solicita ao usuário selecionar a planilha do Excel
        arquivo = askopenfilename(title='Selecione a planilha Excel', filetypes=[('Excel files', '*.xlsx;*.xls')])
        
        if not arquivo:
            self.stdout.write(self.style.ERROR('Nenhum arquivo selecionado.'))
            logging.warning('Nenhum arquivo selecionado.')
            return

        try:
            # Lê o arquivo Excel
            df = pd.read_excel(arquivo)
            logging.info('Arquivo Excel lido com sucesso.')

            # Verificar se as colunas 'id', 'nome', e 'estado' estão presentes
            if not all(col in df.columns for col in ['id', 'nome', 'estado']):
                raise ValueError("As colunas 'id', 'nome', ou 'estado' não foram encontradas no arquivo Excel.")

            for index, row in df.iterrows():
                try:
                    # Verificar se o ID está presente e é válido
                    if pd.isna(row['id']) or not isinstance(row['id'], (int, float)):
                        raise ValueError(f"ID inválido na linha {index + 1}")

                    # Obter o Estado relacionado com base no ID
                    estado_id = row['estado']
                    estado = Estado.objects.filter(id=estado_id).first()

                    if not estado:
                        raise ValueError(f"Estado com ID {estado_id} não encontrado para a cidade na linha {index + 1}")

                    # Preencher os campos do modelo Cidade
                    cidade = Cidade(
                        id=int(row['id']),  # Convertendo ID para inteiro
                        nome=str(row['nome']).strip() if pd.notna(row['nome']) else None,
                        estado=estado  # Relacionando com o estado
                    )
                    cidade.save()
                    logging.info(f'Cidade {cidade.nome} (ID: {cidade.id}) importada com sucesso.')
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao importar Cidade na linha {index + 1}: {e}"))
                    logging.error(f'Erro ao importar Cidade na linha {index + 1}: {e}')

            self.stdout.write(self.style.SUCCESS('Importação de cidades concluída com sucesso!'))
            logging.info('Importação de cidades concluída com sucesso!')
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo Excel: {e}'))
            logging.error(f'Erro ao ler o arquivo Excel: {e}')

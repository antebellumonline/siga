import pandas as pd
from django.core.management.base import BaseCommand
from certificacoes.models import Certificador
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import logging
import os

# Configuração do logging
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'import_certificador-log.txt')

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Command(BaseCommand):
    help = 'Importa os Certificadores de uma planilha Excel'

    def handle(self, *args, **kwargs):
        Tk().withdraw()
        arquivo = askopenfilename(title='Selecione a planilha Excel', filetypes=[('Excel files', '*.xlsx;*.xls')])
        
        if not arquivo:
            self.stdout.write(self.style.ERROR('Nenhum arquivo selecionado.'))
            logging.warning('Nenhum arquivo selecionado.')
            return

        try:
            df = pd.read_excel(arquivo)
            logging.info('Arquivo Excel lido com sucesso.')

            # Verificar se a coluna 'siglaCertificador' existe
            if 'siglaCertificador' not in df.columns:
                raise ValueError("A coluna 'siglaCertificador' não foi encontrada no arquivo Excel.")

            for index, row in df.iterrows():
                try:
                    # Obter a sigla do certificador
                    sigla_certificador = str(row['siglaCertificador']).strip() if pd.notna(row['siglaCertificador']) else None
                    
                    if sigla_certificador:
                        # Salvar o certificador se ele não existir
                        certificador, created = Certificador.objects.get_or_create(siglaCertificador=sigla_certificador)
                        if created:
                            logging.info(f'Novo certificador criado: {certificador.siglaCertificador} na linha {index + 1}.')
                        else:
                            logging.info(f'Certificador existente: {certificador.siglaCertificador} na linha {index + 1}.')
                    else:
                        raise ValueError(f"Sigla inválida na linha {index + 1}")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao importar na linha {index + 1}: {e}"))
                    logging.error(f'Erro ao importar na linha {index + 1}: {e}')

            self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))
            logging.info('Importação concluída com sucesso!')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo Excel: {e}'))
            logging.error(f'Erro ao ler o arquivo Excel: {e}')

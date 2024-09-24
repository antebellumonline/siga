import pandas as pd
from django.core.management.base import BaseCommand
from certificacoes.models import Certificacao, Certificador
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import logging
import os

# Configuração do logging (modificação para salvar na pasta 'logs')
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'import_certificacoes-log.txt')

logging.basicConfig(
    filename=log_file,  # Nome do arquivo de log dentro da pasta 'logs'
    level=logging.INFO,  # Define o nível do log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Command(BaseCommand):
    help = 'Importa certificações de uma planilha Excel'

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

            # Verificar se as colunas necessárias estão presentes
            required_columns = ['id', 'idCertificador', 'descricao', 'siglaExame', 'duracao', 'observacao', 'inativo']
            if not all(col in df.columns for col in required_columns):
                raise ValueError("As colunas necessárias não foram encontradas no arquivo Excel.")

            for index, row in df.iterrows():
                try:
                    # Verificar se o ID está presente e é válido
                    if pd.isna(row['id']):
                        raise ValueError(f"ID inválido na linha {index + 1}")

                    # Obter o Certificador relacionado com base no ID
                    id_certificador = row['idCertificador']
                    certificador = Certificador.objects.filter(id=id_certificador).first()

                    if not certificador:
                        raise ValueError(f"Certificador com ID {id_certificador} não encontrado na linha {index + 1}")

                    # Preencher os campos do modelo Certificacao
                    certificacao = Certificacao(
                        id=str(row['id']),  # Presumindo que o ID é uma string
                        idCertificador=certificador.id,
                        descricao=str(row['descricao']).strip() if pd.notna(row['descricao']) else None,
                        siglaExame=str(row['siglaExame']).strip() if pd.notna(row['siglaExame']) else None,
                        duracao=int(row['duracao']) if pd.notna(row['duracao']) else None,
                        observacao=str(row['observacao']).strip() if pd.notna(row['observacao']) else None,
                        inativo=row.get('inativo', 'False') == 'True'  # Conversão de string para booleano
                    )
                    certificacao.save()
                    logging.info(f'Certificação {certificacao.descricao} (ID: {certificacao.id}) importada com sucesso.')
                
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao importar Certificação na linha {index + 1}: {e}"))
                    logging.error(f'Erro ao importar Certificação na linha {index + 1}: {e}')

            self.stdout.write(self.style.SUCCESS('Importação de certificações concluída com sucesso!'))
            logging.info('Importação de certificações concluída com sucesso!')
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo Excel: {e}'))
            logging.error(f'Erro ao ler o arquivo Excel: {e}')

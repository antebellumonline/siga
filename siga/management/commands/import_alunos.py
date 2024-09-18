import os
import pandas as pd
from django.core.management.base import BaseCommand
from alunos.models import Aluno
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import logging

# Configuração do diretório de logs
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)  # Cria o diretório de logs se não existir

# Configuração do arquivo de log
log_file = os.path.join(log_dir, 'import_log.txt')

# Configuração do logging
logging.basicConfig(
    filename=log_file,  # Nome do arquivo de log
    level=logging.INFO,  # Define o nível do log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Command(BaseCommand):
    help = 'Importa alunos de uma planilha Excel'

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

            for index, row in df.iterrows():
                try:
                    aluno = Aluno(
                        uid=int(row['uid']),
                        nome=str(row['nome']).strip() if pd.notna(row['nome']) else None,
                        cpf=row['cpf'] if pd.notnull(row['cpf']) and row['cpf'] != 0 else None,
                        cep=str(row['cep']).strip() if pd.notna(row['cep']) else None,
                        endereco=str(row['endereco']).strip() if pd.notna(row['endereco']) else None,
                        numero=str(row['numero']).strip() if pd.notna(row['numero']) else None,
                        complemento=str(row['complemento']).strip() if pd.notna(row['complemento']) else None,
                        bairro=str(row['bairro']).strip() if pd.notna(row['bairro']) else None,
                        cidade=int(row['cidade']) if pd.notna(row['cidade']) else None,
                        observacao=str(row['observacao']).strip() if pd.notna(row['observacao']) else None,
                        inativo=bool(row['inativo']) if pd.notna(row['inativo']) else False,
                    )
                    aluno.save()
                    logging.info(f'Aluno {aluno.nome} (UID: {aluno.uid}) importado com sucesso.')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao importar aluno na linha {index + 1}: {e}"))
                    logging.error(f'Erro ao importar aluno na linha {index + 1}: {e}')

            self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))
            logging.info('Importação concluída com sucesso!')
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo Excel: {e}'))
            logging.error(f'Erro ao ler o arquivo Excel: {e}')

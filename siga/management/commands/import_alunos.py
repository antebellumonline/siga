import pandas as pd
from django.core.management.base import BaseCommand
from alunos.models import Aluno
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import logging
import os

# Configuração do logging (modificação para salvar na pasta 'logs')
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'import_alunos-log.txt')

logging.basicConfig(
    filename=log_file,  # Nome do arquivo de log dentro da pasta 'logs'
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

            # Verificar se a coluna 'uid' existe no DataFrame
            if 'uid' not in df.columns:
                raise ValueError("A coluna 'uid' não foi encontrada no arquivo Excel.")

            for index, row in df.iterrows():
                try:
                    # Verificar se o UID está presente e é válido
                    if pd.isna(row['uid']) or not isinstance(row['uid'], (int, float)):
                        raise ValueError(f"UID inválido na linha {index + 1}")

                    # Preencher cidade e cpf com zero (0) caso estejam ausentes ou nulos
                    cidade_valor = row.get('cidade', 0)
                    if pd.isna(cidade_valor):
                        cidade_valor = 0  # Define 0 se a cidade estiver nula

                    cpf_valor = row.get('cpf', 0)
                    if pd.isna(cpf_valor) or cpf_valor == 0:
                        cpf_valor = 0  # Define 0 se o CPF estiver nulo ou for 0

                    aluno = Aluno(
                        uid=int(row['uid']),
                        nome=str(row['nome']).strip() if pd.notna(row['nome']) else None,
                        cpf=cpf_valor,  # Usando 0 para CPF se nulo
                        cep=str(row['cep']).strip() if pd.notna(row['cep']) else None,
                        endereco=str(row['endereco']).strip() if pd.notna(row['endereco']) else None,
                        numero=str(row['numero']).strip() if pd.notna(row['numero']) else None,
                        complemento=str(row['complemento']).strip() if pd.notna(row['complemento']) else None,
                        bairro=str(row['bairro']).strip() if pd.notna(row['bairro']) else None,
                        cidade=int(cidade_valor),  # Usando 0 para cidade se nulo
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

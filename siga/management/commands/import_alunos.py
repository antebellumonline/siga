import pandas as pd
from django.core.management.base import BaseCommand
from apps.alunos.models import Aluno
from apps.local.models import Cidade
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
                    cidade_valor = row.get('cidade', 0) or 0
                    cpf_valor = row.get('cpf', 0) or 0

                    # Buscando a instância de Cidade com base no valor
                    try:
                        cidade_instance = Cidade.objects.get(id=int(cidade_valor))
                    except Cidade.DoesNotExist:
                        logging.warning(f"Cidade com ID {cidade_valor} não encontrada.")
                        cidade_instance, created = Cidade.objects.get_or_create(id='0')
                        
                    aluno = Aluno(
                        uid=int(row['uid']),
                        nome=str(row['nome']).strip().upper() if pd.notna(row['nome']) else '',  # Alteração aqui
                        cpf=cpf_valor,  # Usando 0 para CPF se nulo
                        cep=str(row['cep']).strip()[:8] if pd.notna(row['cep']) else '',
                        endereco=str(row['endereco']).strip() if pd.notna(row['endereco']) else '',
                        numero=str(row['numero']).strip() if pd.notna(row['numero']) else '',
                        complemento=str(row['complemento']).strip() if pd.notna(row['complemento']) else '',
                        bairro=str(row['bairro']).strip() if pd.notna(row['bairro']) else '',
                        cidade=cidade_instance,
                        observacao=str(row['observacao']).strip() if pd.notna(row['observacao']) else '',
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

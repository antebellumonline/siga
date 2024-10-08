import pandas as pd
from django.core.management.base import BaseCommand
from alunos.models import Aluno, AlunoContato, ConfigTpContato
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import logging
import os

# Configuração do logging (modificação para salvar na pasta 'logs')
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'import_aluno_contatos-log.txt')

logging.basicConfig(
    filename=log_file,  # Nome do arquivo de log dentro da pasta 'logs'
    level=logging.INFO,  # Define o nível do log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Command(BaseCommand):
    help = 'Importa contatos dos alunos de uma planilha Excel'

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

            # Verificar se as colunas necessárias existem no DataFrame
            required_columns = ['aluno', 'tipoContato', 'contato', 'detalhe']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Uma ou mais colunas obrigatórias estão faltando: {required_columns}")

            for index, row in df.iterrows():
                try:
                    # Verificar se o aluno existe
                    aluno = Aluno.objects.filter(uid=row['aluno']).first()
                    if not aluno:
                        raise ValueError(f"Aluno com UID {row['aluno']} não encontrado.")

                    # Verificar se o tipo de contato existe
                    tipo_contato = ConfigTpContato.objects.filter(id=row['tipoContato']).first()
                    if not tipo_contato:
                        raise ValueError(f"Tipo de contato com ID {row['tipoContato']} não encontrado.")

                    # Cria ou atualiza o contato do aluno
                    contato = AlunoContato.objects.create(
                        aluno=aluno,
                        tipoContato=tipo_contato,
                        contato=str(row['contato']).strip(),
                        detalhe=str(row['detalhe']).strip() if pd.notna(row['detalhe']) else ''
                    )
                    logging.info(f"Contato do aluno {aluno.nome} importado com sucesso.")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao importar contato na linha {index + 1}: {e}"))
                    logging.error(f"Erro ao importar contato na linha {index + 1}: {e}")

            self.stdout.write(self.style.SUCCESS('Importação de contatos concluída com sucesso!'))
            logging.info('Importação de contatos concluída com sucesso!')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo Excel: {e}'))
            logging.error(f'Erro ao ler o arquivo Excel: {e}')

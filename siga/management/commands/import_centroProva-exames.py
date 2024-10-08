import pandas as pd
from django.core.management.base import BaseCommand
from certificacoes.models import Certificacao
from alunos.models import Aluno
from centroProva.models import CentroProva, CentroProvaExame
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import logging
import os
from datetime import datetime

# Configuração do logging (modificação para salvar na pasta 'logs')
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'import_centroProva-exames-log.txt')

logging.basicConfig(
    filename=log_file,  # Nome do arquivo de log dentro da pasta 'logs'
    level=logging.INFO,  # Define o nível do log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Command(BaseCommand):
    help = 'Importa dados dos exames de uma planilha Excel para a tabela CentroProvaExame'

    def add_arguments(self, parser):
        # O argumento '--verbose' para mostrar mais detalhes ao importar
        parser.add_argument('--verbose', action='store_true', help='Mostra informações detalhadas durante a importação')

    def handle(self, *args, **kwargs):
        verbose = kwargs['verbose']

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
            required_columns = ['certificacao', 'centroProva', 'aluno', 'data', 'presenca', 'cancelado', 'inativo']
            if not all(col in df.columns for col in required_columns):
                raise ValueError(f"Uma ou mais colunas obrigatórias estão faltando: {required_columns}")

            for index, row in df.iterrows():
                try:
                    # Verificar se a certificação existe
                    certificacao = Certificacao.objects.filter(id=row['certificacao']).first()
                    if not certificacao:
                        raise ValueError(f"Certificação com ID {row['certificacao']} não encontrada.")

                    # Verificar se o centro de prova existe
                    centro_prova = CentroProva.objects.filter(id=row['centroProva']).first()
                    if not centro_prova:
                        raise ValueError(f"Centro de Prova com ID {row['centroProva']} não encontrado.")

                    # Verificar se o aluno existe
                    aluno = Aluno.objects.filter(id=row['aluno']).first()
                    if not aluno:
                        raise ValueError(f"Aluno com ID {row['aluno']} não encontrado.")

                    # Verificar e formatar a data
                    try:
                        data_exame = pd.to_datetime(row['data']).date()
                    except Exception:
                        raise ValueError(f"Data inválida no exame na linha {index + 1}: {row['data']}")

                    # Converter os campos booleanos para o formato correto
                    presenca = bool(row['presenca'])
                    cancelado = bool(row['cancelado'])
                    inativo = bool(row['inativo'])

                    # Criar ou atualizar o registro do exame
                    exame = CentroProvaExame.objects.create(
                        certificacao=certificacao,
                        centroProva=centro_prova,
                        aluno=aluno,
                        data=data_exame,
                        presenca=presenca,
                        cancelado=cancelado,
                        inativo=inativo
                    )
                    logging.info(f"Exame do aluno {aluno.nome} importado com sucesso.")

                    if verbose:
                        self.stdout.write(self.style.SUCCESS(f"Exame do aluno {aluno.nome} na linha {index + 1} importado com sucesso."))

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao importar exame na linha {index + 1}: {e}"))
                    logging.error(f"Erro ao importar exame na linha {index + 1}: {e}")

            self.stdout.write(self.style.SUCCESS('Importação de exames concluída com sucesso!'))
            logging.info('Importação de exames concluída com sucesso!')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo Excel: {e}'))
            logging.error(f'Erro ao ler o arquivo Excel: {e}')

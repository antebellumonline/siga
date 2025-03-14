from tkinter import Tk
from tkinter.filedialog import askopenfilename

import logging
import os

import pandas as pd
from django.core.management.base import BaseCommand
from apps.empresas.models import Empresa
from apps.local.models import Cidade

# Configuração do logging (modificação para salvar na pasta 'logs')
log_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'import_empresas-log.txt')

logging.basicConfig(
    filename=log_file,  # Nome do arquivo de log dentro da pasta 'logs'
    level=logging.INFO,  # Define o nível do log
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Command(BaseCommand):
    help = 'Importa empresas de uma planilha Excel'

    def handle(self, *args, **kwargs):
        # Oculta a janela principal do Tkinter
        Tk().withdraw()

        # Solicita ao usuário selecionar a planilha do Excel
        arquivo = askopenfilename(
            title='Selecione a planilha Excel',
            filetypes=[('Excel files', '*.xlsx;*.xls')]
        )

        if not arquivo:
            self.stdout.write(self.style.ERROR('Nenhum arquivo selecionado.'))
            logging.warning('Nenhum arquivo selecionado.')
            return

        try:
            # Lê o arquivo Excel
            df = pd.read_excel(arquivo, dtype={'taxId': str})
            logging.info('Arquivo Excel lido com sucesso.')

            # Verificar se a coluna 'taxId' existe no DataFrame
            if 'taxId' not in df.columns:
                raise ValueError("A coluna 'taxId' não foi encontrada no arquivo Excel.")

            for index, row in df.iterrows():
                try:
                    # Verificar se o taxId está presente e é válido
                    tax_id = str(row['taxId']).strip()
                    if not tax_id.isdigit():
                        raise ValueError(f"Tax ID inválido na linha {index + 1}: {tax_id}")

                    # Preencher cidade com zero (0) caso estejam ausentes ou nulos
                    cidade_valor = row.get('cidade', 0) or 0

                    # Buscando a instância de Cidade com base no valor
                    try:
                        cidade_instance = Cidade.objects.get(id=int(cidade_valor))
                    except Cidade.DoesNotExist:
                        logging.warning(f"Cidade com ID {cidade_valor} não encontrada.")
                        cidade_instance, created = Cidade.objects.get_or_create(id='0')

                    empresa = Empresa(
                        taxId=tax_id,
                        razaoSocial=str(
                            row['razaoSocial']
                        ).strip().upper() if pd.notna(row['razaoSocial']) else '',
                        fantasia=str(
                            row['fantasia']
                        ).strip().upper() if pd.notna(row['fantasia']) else '',
                        cep=str(row['cep']).strip()[:8] if pd.notna(row['cep']) else '',
                        endereco=str(row['endereco']).strip() if pd.notna(row['endereco']) else '',
                        numero=str(row['numero']).strip() if pd.notna(row['numero']) else '',
                        complemento=str(
                            row['complemento']
                        ).strip() if pd.notna(row['complemento']) else '',
                        bairro=str(row['bairro']).strip() if pd.notna(row['bairro']) else '',
                        cidade=cidade_instance,
                        observacao=str(
                            row['observacao']
                        ).strip() if pd.notna(row['observacao']) else '',
                        inativo=bool(row['inativo']) if pd.notna(row['inativo']) else False,
                    )
                    empresa.save()
                    logging.info(f'Empresa {empresa.razaoSocial} (Tax ID: {empresa.taxId}) importada com sucesso.')
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao importar empresa na linha {index + 1}: {e}"))
                    logging.error(f'Erro ao importar empresa na linha {index + 1}: {e}')

            self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso!'))
            logging.info('Importação concluída com sucesso!')

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo Excel: {e}'))
            logging.error(f'Erro ao ler o arquivo Excel: {e}')

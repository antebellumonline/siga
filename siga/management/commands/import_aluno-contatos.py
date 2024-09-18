import pandas as pd
from django.core.management.base import BaseCommand
from alunos.models import Aluno, ConfigTpContato, AlunoContato  # Importações corrigidas
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import logging

# Configura o logger para registrar informações em um arquivo
logging.basicConfig(
    filename='import_aluno_contatos.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
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
            logging.error('Nenhum arquivo selecionado.')
            return

        try:
            # Lê o arquivo Excel
            df = pd.read_excel(arquivo)

            for index, row in df.iterrows():
                try:
                    # Verifica ou cria o tipo de contato
                    tipo_contato, created = ConfigTpContato.objects.get_or_create(
                        descricao=row['tipo_contato'],
                        defaults={'inativo': False}
                    )

                    if created:
                        logging.info(f"Tipo de contato '{row['tipo_contato']}' criado.")
                    
                    # Associa o contato ao aluno
                    aluno = Aluno.objects.get(UID=int(row['UID']))

                    aluno_contato = AlunoContato(
                        aluno=aluno,
                        tipo_contato=tipo_contato,
                        contato=str(row['contato']).strip(),
                        detalhe=str(row['detalhe']).strip() if pd.notna(row['detalhe']) else None,
                    )
                    aluno_contato.save()
                    
                    logging.info(f"Contato importado com sucesso para o aluno {aluno.nome} (UID {aluno.UID}).")

                except Aluno.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Aluno com UID {row['UID']} não encontrado na linha {index + 1}."))
                    logging.error(f"Aluno com UID {row['UID']} não encontrado na linha {index + 1}.")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Erro ao importar contato na linha {index + 1}: {e}"))
                    logging.error(f"Erro ao importar contato na linha {index + 1}: {e}")

            self.stdout.write(self.style.SUCCESS('Importação de contatos concluída com sucesso!'))
            logging.info('Importação de contatos concluída com sucesso!')
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao ler o arquivo Excel: {e}'))
            logging.error(f'Erro ao ler o arquivo Excel: {e}')

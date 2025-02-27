import os
import sys
import subprocess
from datetime import datetime

def generate_diagram():
    # Define o diretório e o nome do arquivo
    directory = r"C:\Users\AndreVentura\ANTEBELLUM LLC\SIGA - Documentos\Diagramas"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Obtém a data e hora atual
    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M")

    # Define o nome do arquivo com a data e hora atual
    file_name = f"siga-app_diagrama_{date_time}.pdf"
    file_path = os.path.join(directory, file_name)

    # Muda para o diretório do projeto
    os.chdir(r'C:\Users\AndreVentura\ANTEBELLUM LLC\SIGA - Documentos\siga-app')

    # Gera o diagrama em formato PDF
    result = subprocess.run([sys.executable, "manage.py", "graph_models", "-a", "--group-models", "-o", file_path],
                        capture_output=True, text=True)


    # Verifica se houve algum erro durante a execução do comando
    if result.returncode != 0:
        print("Erro ao gerar o diagrama:")
        print(result.stderr)
    else:
        print(f"Diagrama gerado com sucesso: {file_path}")

if __name__ == "__main__":
    generate_diagram()

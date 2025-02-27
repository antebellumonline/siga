import os
import sys
import django
import subprocess

from django.conf import settings
from datetime import datetime

# Define o DJANGO_SETTINGS_MODULE antes de chamar django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "siga.settings")
django.setup()

def get_project_apps():
    return [
        app.split('.')[-1]
        for app in settings.INSTALLED_APPS
        if not app.startswith("django.") and not app.startswith("allauth")
    ]
apps = get_project_apps()

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
    result = subprocess.run([sys.executable, "manage.py", "graph_models", *apps, "--group-models", "-o", file_path],
                        capture_output=True, text=True)

    # Verifica se houve algum erro durante a execução do comando
    if result.returncode != 0:
        print("Erro ao gerar o diagrama:")
        print(result.stderr)
    else:
        print(f"Diagrama gerado com sucesso: {file_path}")

if __name__ == "__main__":
    generate_diagram()

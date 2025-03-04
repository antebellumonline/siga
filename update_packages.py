"""
Script para atualizar pacotes desatualizados no ambiente virtual Python e
gerar um novo arquivo requirements.txt com as versões atualizadas.

O script executa os seguintes passos:
1. Verifica quais pacotes estão desatualizados.
2. Atualiza somente os pacotes desatualizados.
3. Regenera o arquivo requirements.txt com as versões mais recentes dos pacotes.
"""

import subprocess

def run_command(command):
    """
    Executa um comando no terminal e retorna o resultado.
    
    Args:
        command (str): O comando a ser executado no terminal.

    Returns:
        str: Saída do comando.
    """
    result = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, shell=True, check=True
    )
    return result.stdout

def update_packages():
    """
    Atualiza os pacotes desatualizados no ambiente virtual e
    gera um novo arquivo 'requirements.txt' com as versões atualizadas.
    """
    # Rodar pip list --outdated para pegar pacotes desatualizados
    result = subprocess.run(
        "pip list --outdated", stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
        text=True, shell=True, check=True
    )

    outdated_packages = result.stdout.splitlines()[2:]  # Ignora as primeiras duas linhas (header)

    if not outdated_packages:
        print("Não há pacotes desatualizados.")
        return

    print(f"Pacotes desatualizados encontrados: {len(outdated_packages)}")

    # Atualizando os pacotes desatualizados
    for package in outdated_packages:
        package_name = package.split()[0]
        print(f"Atualizando {package_name}...")
        run_command(f"pip install --upgrade {package_name}")

    # Regenerar o requirements.txt com as versões atualizadas
    print("\nAtualizando o requirements.txt...")
    run_command("pip freeze > requirements.txt")
    print("Atualização concluída com sucesso!")

if __name__ == "__main__":
    update_packages()

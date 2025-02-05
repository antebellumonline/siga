"""
Módulo para gerar uma estrutura de diretórios no formato de árvore
e salvá-la em um arquivo Markdown. Este módulo é utilizado para
documentar a estrutura do Projeto SIGA.
"""

import os

def generate_tree(directory, prefix=''):
    """
    Gera uma string com a estrutura de diretórios no formato de árvore,
    ignorando arquivos indesejados.

    Args:
        directory (str): O caminho do diretório a ser explorado.
        prefix (str): O prefixo utilizado para formatação da árvore.

    Returns:
        str: Representação em formato de árvore da estrutura de diretórios.
    """
    tree_str = ''
    items = os.listdir(directory)

    # Lista de extensões e nomes de arquivos a ignorar
    ignore_files = ['.git',
                    '__pycache__',
                    '.DS_Store',
                    'venv',
                    'env',
                    'node_modules',
                    'sigaenv',
                    'build',
                    'dist',
                    'htmlcov',
                    'coverage',
                    'structure.md',
                    'staticfiles'
                ]

    # Lista de extensões e nomes de arquivos a incluir
    include_files = ['.py',
                     '.md',
                     '.sh',
                     '.txt',
                     '.rst',
                     '.html',
                     '.css',
                     '.js',
                     '.png',
                     '.jpg',
                     '.jpeg',
                     '.gif',
                     '.svg',
                     '.woff',
                     '.woff2',
                     '.ttf',
                     '.eot',
                     '.mp4',
                     '.webm'
                    ]

    for index, item in enumerate(items):
        path = os.path.join(directory, item)

        # Ignora diretórios ou arquivos que estão na lista de ignorados
        if item in ignore_files or item.startswith('.'):
            continue

        # Verifica se o item é um diretório ou um arquivo com extensão permitida
        if os.path.isdir(path) or any(item.endswith(ext) for ext in include_files):
            is_last = index == len(items) - 1
            connector = '└── ' if is_last else '├── '
            tree_str += prefix + connector + item + '\n'

            if os.path.isdir(path):
                # Chama recursivamente para subdiretórios
                tree_str += generate_tree(path, prefix + ('    ' if is_last else '│   '))

    return tree_str

def main():
    """
    Função principal que gera a estrutura do projeto Django e a escreve
    em um arquivo Markdown.

    O diretório do projeto é determinado a partir do caminho relativo
    do script.
    """
    # Caminho do diretório do projeto Django
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "siga-app"))

    # Gera a estrutura da árvore
    project_tree = generate_tree(project_dir)

    # Caminho para o arquivo Markdown que será gerado
    markdown_file = os.path.join(project_dir, "structure.md")

    # Escreve a estrutura da árvore no arquivo Markdown
    with open(markdown_file, 'w', encoding='utf-8') as md_file:
        md_file.write("# Estrutura do Projeto Django\n\n")
        md_file.write("```plaintext\n")
        md_file.write(project_tree)
        md_file.write("```\n")

    print(f"Arquivo Markdown gerado em: {markdown_file}")

if __name__ == "__main__":
    main()

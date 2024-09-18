import os

def generate_tree(directory, prefix=''):
    """
    Gera uma string com a estrutura de diretórios no formato de árvore, ignorando arquivos indesejados.
    """
    tree_str = ''
    items = os.listdir(directory)
    
    # Lista de extensões e nomes de arquivos a ignorar
    ignore_files = ['.git', '__pycache__', '.DS_Store', 'venv', 'env', 'node_modules']
    
    for index, item in enumerate(items):
        path = os.path.join(directory, item)
        
        # Ignora diretórios ou arquivos que estão na lista de ignorados
        if item in ignore_files or item.startswith('.'):
            continue
        
        is_last = index == len(items) - 1
        connector = '└── ' if is_last else '├── '
        tree_str += prefix + connector + item + '\n'
        
        if os.path.isdir(path):
            # Chama recursivamente para subdiretórios
            tree_str += generate_tree(path, prefix + ('    ' if is_last else '│   '))
    
    return tree_str

def main():
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

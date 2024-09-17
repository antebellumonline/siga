import os
import pandas as pd
import pyodbc
from dotenv import load_dotenv
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações de conexão do SQL Server usando variáveis de ambiente
server = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

# String de conexão com o SQL Server
connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Função para importar dados do Excel para o SQL Server
def import_excel_to_sql(file_path, table_name):
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(file_path)

        # Conectar ao SQL Server
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Iterar sobre o DataFrame e inserir os dados no banco
        for index, row in df.iterrows():
            columns = ', '.join(row.index)
            values = ', '.join(['?'] * len(row))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            cursor.execute(sql, tuple(row))

        # Commit das inserções
        conn.commit()
        cursor.close()
        conn.close()

        print(f"Dados importados com sucesso para a tabela {table_name}")

    except Exception as e:
        print(f"Erro ao importar dados: {e}")

def select_file():
    # Cria uma janela oculta para usar o diálogo de arquivo
    Tk().withdraw() 
    file_path = askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    return file_path

# Chamada da função
if __name__ == "__main__":
    # Solicitar ao usuário para selecionar o arquivo Excel
    file_path = select_file()

    if file_path:
        # Nome da tabela no SQL Server (alterar conforme necessário)
        table_name = 'nome_da_sua_tabela'
        
        # Executar a importação
        import_excel_to_sql(file_path, table_name)
    else:
        print("Nenhum arquivo selecionado.")
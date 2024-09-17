import pyodbc

conn_str = (
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=siga-database-server.database.windows.net;'
    'DATABASE=siga-database;'
    'UID=administrador;'
    'PWD=p@c3mBellum'
)

try:
    conn = pyodbc.connect(conn_str)
    print("Conexão bem-sucedida!")
    conn.close()
except Exception as e:
    print(f"Erro ao conectar: {e}")

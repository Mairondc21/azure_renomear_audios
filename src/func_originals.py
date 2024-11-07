import pyodbc
import pandas as pd
from pathlib import Path

def get_tabela_do_azure() -> pd.DataFrame:
    server = 'sql-expertise-01.database.windows.net'
    database = 't_imag_o2_2024'
    username = 'igor.giori'
    password = 'Danae!@2023'
    table_name = 'dbo.entrevistas'
    # Construa a string de conexão
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

    try:
        # Conecte-se ao banco de dados
        with pyodbc.connect(connection_string) as conn:
            # Execute a consulta para capturar a tabela
            query = f"SELECT * FROM {table_name} WHERE OK IS NOT NULL"
            df = pd.read_sql(query, conn)
            df = df[['codigo_entrevistado','DDD','TELEFONE','DDD2','FONE2','DDD3','FONE3','Q8A']]
            return df
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None


    return df

def renomear_audios(base: pd.DataFrame, caminho_audios: Path) -> None:
    df = base['codigo_entrevistado']



# função que lê do azure e trasforma em dataframe
df_azure = get_tabela_do_azure()

print(df_azure)
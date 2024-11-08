import pyodbc
import pandas as pd
from pathlib import Path
import datetime
from dotenv import load_dotenv
import os

def load_settings():
    """Carrega as configurações a partir de variáveis de ambiente."""
    dotenv_path = Path.cwd() / '.env'
    load_dotenv(dotenv_path=dotenv_path)

    settings = {
        "db_server": os.getenv("SSMS_SERVER"),
        "db_db": os.getenv("SSMS_DB"),
        "db_user": os.getenv("SSMS_USER"),
        "db_pass": os.getenv("SSMS_PASS"),
        "db_table": os.getenv("SSMS_TABLE"),
    }
    return settings


def get_tabela_do_azure() -> pd.DataFrame:

    settings = load_settings()
    # Construa a string de conexão
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={settings['db_server']};DATABASE={settings['db_db']};UID={settings['db_user']};PWD={settings['db_pass']}"

    local_time = datetime.datetime.now()
    tempo = local_time.strftime('%Y%m%d%H%M')
    try:
        # Conecte-se ao banco de dados
        with pyodbc.connect(connection_string) as conn:
            # Execute a consulta para capturar a tabela
            query = f"SELECT * FROM {settings['db_table']} WHERE ok IS NOT NULL AND ULT_RESP ='TERMO' AND Q7 IS NOT NULL"
            df = pd.read_sql(query, conn)
            df = df[['codigo_entrevistado','DDD','TELEFONE','DDD2','FONE2','DDD3','FONE3','Q8A','Q7']]

            pd.set_option('display.float_format', '{:.0f}'.format)
            df = df.to_excel(f'dados//bd_{tempo}.xlsx')        
            return df
    except Exception as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None


    return df

def renomear_audios(base: pd.DataFrame, caminho_audios: Path, caminho_out: Path) -> None:
    lista_paths = os.listdir(caminho_audios)
    df = pd.read_excel(base)
    for path in lista_paths:
        caminho_path = os.path.join(caminho_audios,path)
        arquivos = os.listdir(caminho_path)
        if len(arquivos) > 0:
            for arquivo in arquivos:
                if arquivo.endswith(".WAV"):
                    caminho_subarquivos = os.path.join(caminho_path, arquivo)
                    nome_completo = os.path.basename(caminho_subarquivos)
                    nome_completo_separado = nome_completo.split("_")
                    if 'q8q8a' in nome_completo_separado:
                        nome = nome_completo_separado[1]
                        extensao = os.path.splitext(nome_completo)[1]
                    else:
                        continue
                else:
                    continue
                try:
                   for index, row in df.astype(str).iterrows():
                        # Verificar se o nome está em uma das três colunas
                        if nome == row['Tel_1'] or nome == row['Tel_2'] or nome == row['Tel_3']:
                            #nome adicionando a pasta de dia para saber qual dia foi da pasta
                            #novo_nome = f"{caminho_out}//{path}_{row['Cod']}_{row['OPS']}_{row['NPS']}.WAV"
                            novo_nome = f"{caminho_out}//{row['Cod']}_{row['OPS']}_{row['NPS']}.WAV"
                            novo_caminho = os.path.join(caminho_audios,novo_nome)
                            os.rename(caminho_subarquivos,novo_caminho)
                except Exception as e:
                    print(f"Unexpected {e=}, {type(e)=}")
        else:
            continue



# função que lê do azure e trasforma em arquivo excel
df_azure = get_tabela_do_azure()

destino_arquivos_tratados = r'C:\Users\mairon.costa\OneDrive - Expertise Inteligência e Pesquisa de Mercado\expertise_mairon\2024\postmetria\audios_driver\OUT\nps_ok_ult-resp_not_null'
audios = r'C:\Users\mairon.costa\OneDrive - Expertise Inteligência e Pesquisa de Mercado\expertise_mairon\2024\postmetria\audios_driver\IN\11'
base_df = "./dados/bd_202411081235.xlsx"
#renomear_audios(base_df,audios,destino_arquivos_tratados)
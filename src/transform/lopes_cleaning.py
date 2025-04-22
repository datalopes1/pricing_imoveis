import pandas as pd
import duckdb 
from datetime import datetime
import uuid

def gerar_id():
    """
    Função para criação de um UUID4 para cada linha do DataFrame
    """
    return str(uuid.uuid4())

df = pd.read_json("data/raw/lopes.json")

# Limpeza de nulos e duplicados
df.dropna(subset='preco', inplace=True)
df.drop_duplicates(inplace=True)

# Limpeza das colunas com dtype FLOAT
for col in ['preco', 'condo']:
    df.fillna({col: '0'}, inplace=True)
    df[col] = df[col].astype(str).str.replace('[^0-9]', '', regex=True)
    df[col] = df[col].astype(float)

# Limpeza das colunas com dtype INT
for col in ['area', 'quartos', 'banheiros', 'vagas']:
    df.fillna({col: 0}, inplace=True)
    df[col] = df[col].astype(str).str.replace('[^0-9d]', '', regex=True)
    df[col] = df[col].astype(int)

# Limpeza na localização
df['localizacao'] = df['localizacao'].astype(str).str.split(',', expand=True)[1]
df['localizacao'] = df['localizacao'].astype(str).str.split('-', expand=True)[0]
df['localizacao'] = df['localizacao'].astype(str).str.strip()

# Adição de metadados
df['origem'] = 'Lopes'
df['timestamp_extracao'] = datetime.now()
df['id'] = df.apply(lambda row: gerar_id(), axis=1)

# Finalização da limpeza e salvamento em .csv
df = duckdb.sql(
    """
    SELECT 
        id
        , origem
        , tipo
        , CASE 
            WHEN LOWER(localizacao) LIKE '%praia do futuro%' THEN 'Praia do Futuro' 
            ELSE localizacao 
        END AS localizacao
        , area
        , quartos
        , banheiros
        , vagas
        , condo
        , preco
        , ROUND((preco/area)::DECIMAL, 2) AS preco_m2
        , timestamp_extracao
    FROM df
    WHERE
        area >= 34
        AND quartos > 0
        AND banheiros > 0
        AND preco >= 70000
        AND quartos <= 10
    """
).df()

df.to_csv("data/processed/lopes.csv", index=False)
print(df.head())
print(df.info())
print(f"\nDados salvos na pasta data/processed/")

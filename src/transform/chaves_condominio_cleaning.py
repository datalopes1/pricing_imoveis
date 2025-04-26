import pandas as pd
import duckdb 
from datetime import datetime
import uuid

def gerar_id():
    """
    Função para criação de um UUID4 para cada linha do DataFrame
    """
    return str(uuid.uuid4())

df = pd.read_json("data/raw/chaves_condominio.json")

for col in ['preco', 'condo']:
    df.fillna({col: '0'}, inplace=True)
    df[col] = df[col].astype(str).str.replace('[^0-9]', '', regex=True)
    df[col] = df[col].replace('', '0')
    df[col] = df[col].astype(float)

for col in ['area', 'quartos', 'banheiros', 'vagas']:
    df.fillna({col: '0'}, inplace=True)
    df[col] = df[col].astype(int)

df['localizacao'] = df['localizacao'].astype(str).str.split(',', expand=True)[0]

# Adição de metadados
df['origem'] = 'Chaves na Mão'
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
            WHEN LOWER(localizacao) LIKE '%conjunto ceará%' THEN 'Conjunto Ceará'
            WHEN LOWER(localizacao) LIKE '%coité%' THEN 'Coité' 
            ELSE localizacao 
        END AS localizacao
        , CASE 
            WHEN localizacao IN ('Barra do Ceará', 'Jacarecanga', 'Pirambu', 'Cristo Redentor', 'Carlito Pamplona', 'Jardim Iracema', 'Floresta', 'Álvaro Weyne', 'Vila Velha') THEN 'SER1'
            WHEN localizacao IN ('Aldeota', 'Meireles', 'Varjota', 'Papicu', 'Mucuripe', 'Cais do Porto', 'Joaquim Távora', 'Dionísio Torres', 'São João do Tauape', 'Dionisio Torres', 'de Lourdes', 'Vicente Pinzon') THEN 'SER2'
            WHEN localizacao IN ('Rodolfo Teófilo','São Gerardo','Antônio Bezerra', 'Quintino Cunha', 'Olavo Oliveira', 'Padre Andrade', 'Presidente Kennedy', 'Vila Ellery', 'Monte Castelo', 'Amadeu Furtado', 'Farias Brito', 'Parquelândia') THEN 'SER3'
            WHEN localizacao IN ('Benfica', 'José Bonifácio', 'Fátima', 'Damas', 'Parangaba', 'Vila Peri', 'Aeroporto', 'Montese', 'Vila União') THEN 'SER4'
            WHEN localizacao IN ('Granja Lisboa', 'Granja Portugal', 'Bom Jardim', 'Siqueira', 'Bonsucesso') THEN 'SER5'
            WHEN localizacao IN ('Paupina','Jardim das Oliveiras','Cidade dos Funcionários', 'Parque Manibura', 'Cambeba', 'Messejana', 'Curió', 'Lagoa Redonda', 'Alto da Balança', 'Coaçu', 'José de Alencar', 'São Bento', 'Parque Iracema') THEN 'SER6'
            WHEN localizacao IN ('Patriolino Ribeiro','Praia do Futuro', 'Cocó', 'Cidade 2000', 'Sabiaguaba', 'Edson Queiroz', 'Guararapes', 'Engenheiro Luciano Cavalcante', 'Sapiranga', 'Manoel Dias Branco') THEN 'SER7'
            WHEN localizacao IN ('Serrinha', 'Boa Vista', 'Parque Dois Irmãos', 'Passaré', 'Prefeito José Walter', 'Castelão', 'Boa Vista Castelão', 'Dias Macedo','Dendê', 'Itaperi', 'Planalto Ayrton Senna') THEN 'SER8'
            WHEN localizacao IN ('Cajazeiras', 'Barroso', 'Conjunto Palmeiras', 'Jangurussu', 'Parque Santa Maria', 'Ancuri', 'Pedras') THEN 'SER9'
            WHEN localizacao IN ('Mondubim', 'Canindezinho', 'Parque São José', 'Conjunto Esperança', 'Maraponga', 'Novo Mondubim', 'Jardim Cearense') THEN 'SER10'
            WHEN localizacao IN ('Pici', 'Bela Vista', 'Couto Fernandes', 'Henrique Jorge', 'Genibaú', 'Conjunto Ceará', 'Democrito Rocha', 'Dom Lustosa', 'João Xxiii') THEN 'SER11'
            WHEN localizacao IN ('Jóquei Clube','Centro', 'Moura Brasil', 'Praia de Iracema') THEN 'SER12'
		    ELSE 'Outros'
	    END AS ser
        , CASE
            WHEN localizacao IN ('Benfica', 'José Bonifácio', 'Joaquim Távora', 'Aldeota', 'Meireles', 'Jacarecanga', 'Farias Brito', 'Praia de Iracema', 'Moura Brasil') THEN 'Sim'
            ELSE 'Não'
        END AS prox_centro
        , CASE
            WHEN localizacao IN ('Praia do Futuro', 'Meireles', 'Mucuripe', 'Praia de Iracema', 'Barra do Ceará', 'Cais do Porto', 'Sabiaguaba') THEN 'Sim'
            ELSE 'Não'
        END AS prox_orla
        , area
        , quartos
        , banheiros
        , vagas
        , condo
        , preco
        , timestamp_extracao
    FROM df
    WHERE
        area >= 34
        AND quartos > 0
        AND banheiros > 0
        AND preco >= 70000
    """
).to_df()

df.to_csv("data/interim/chaves_condominio.csv", index=False)
print(df.head())
print(df.info())
print(f"\nDados salvos na pasta data/processed/")
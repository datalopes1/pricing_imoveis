import pandas as pd
import sqlite3

conn = sqlite3.connect("data/imv_database.db")

lopes = pd.read_csv("data/processed/lopes.csv")
lopes.to_sql("raw_imoveis", conn, if_exists='replace', index=False, method='multi')

chaves_1 = pd.read_csv("data/processed/chaves_apts.csv")
chaves_2 = pd.read_csv("data/processed/chaves_casas.csv")
chaves_3 = pd.read_csv("data/processed/chaves_condominio.csv")
chaves = pd.concat([chaves_1, chaves_2, chaves_3])
chaves.to_sql("raw_imoveis", conn, if_exists='append', index=False, method='multi')

print("\nCriação do banco de dados sqlite3 e ingestão de dados completa.")
conn.close()

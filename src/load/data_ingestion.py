import pandas as pd
import sqlite3

conn = sqlite3.connect("data/imv_database.db")

lopes = pd.read_csv("data/processed/lopes.csv")
lopes.to_sql("raw_imoveis", conn, if_exists='replace', index=False, method='multi')

chaves = pd.read_csv("data/processed/chaves.csv")
chaves.to_sql("raw_imoveis", conn, if_exists='append', index=False, method='multi')

print("\nCriação do banco de dados sqlite3 e ingestão de dados completa.")
conn.close()

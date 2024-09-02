# Importar as bibliotecas necessárias
import pandas as pd
import sqlite3
from datetime import datetime

# Ler os dados do arquivo JSON
df = pd.read_json('../data/data_mercadolivre.jsonl', lines=True)

# Converter coluna para datetime
df['date_created'] = pd.to_datetime(df['date_created'], errors='coerce')  # Usa 'coerce' para tratar valores inválidos

# Preencher valores nulos com 0 e converter para float
df['old_price_reais'] = df['old_price_reais'].fillna(0).astype(float)
df['old_price_centavos'] = df['old_price_centavos'].fillna(0).astype(float)
df['new_price_reais'] = df['new_price_reais'].fillna(0).astype(float)
df['new_price_centavos'] = df['new_price_centavos'].fillna(0).astype(float)  # Corrigido para 'new_price_centavos'
df['reviews_rating_number'] = df['reviews_rating_number'].fillna(0).astype(float)
# Extrair números de dentro dos parênteses na coluna 'reviews_amount', preencher valores nulos com 0 e converter para inteiro
df['reviews_amount'] = df['reviews_amount'].str.replace(r'[\(\)]', '', regex=True)
df['reviews_amount'] = df['reviews_amount'].fillna(0).astype(int)

# Tratar colunas de preços, unificando e tornando o preço correto
df['old_price'] = df['old_price_reais'] + df['old_price_centavos'] / 100
df['new_price'] = df['new_price_reais'] + df['new_price_centavos'] / 100

# Remover colunas antigas dos preços
df.drop(columns=['old_price_reais', 'old_price_centavos', 'new_price_reais', 'new_price_centavos'], inplace=True)

# Conectar o banco de dadps SQlite
conn = sqlite3.connect('../data/ScrapeStore.db')

# Salvar o DataFrame no banco mercado_livre.db no SQLite
df.to_sql('mercadolivre_products', conn, if_exists='replace', index=False)

# Encerrar conexão com o banco de dados
conn.close()

# Exibir DataFrame
print(df)
# -------------------------------------------------------------------------------
#  ESTE ARQUIVO CARREGA OS DADOS ORIGINAIS DO DATASET PARA A TABELA "raw_vendas"
#--------------------------------------------------------------------------------

# Configurações:
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from conexao import engine_supermarket

# Caminho do dataset original:
CAMINHO_CSV = Path(__file__).resolve().parent.parent / "data" / "raw" / "supermarket_data_original.csv"

# Leitura do csv:
df_supermarket = pd.read_csv(CAMINHO_CSV)

# Padronização dos nomes das colunas (mesmos nomes da tabela raw_vendas):
df_supermarket.columns = [
    "invoice_id", "branch", "city", "customer_type", "gender",
    "product_line", "unit_price", "quantity", "tax_5", "total",
    "date", "time", "payment", "cogs", "gross_margin_percentage",
    "gross_income", "rating",
]

# Limpa a tabela para evitar duplicidade caso o script rode mais de uma vez:
with engine_supermarket.begin() as conexao:
    conexao.execute(text("TRUNCATE TABLE raw_vendas"))

# Carga dos dados na tabela raw_vendas:
df_supermarket.to_sql(
    "raw_vendas",
    engine_supermarket,
    if_exists="append",
    index=False,
)

print(f"{len(df_supermarket)} registros carregados em raw_vendas.")
# -------------------------------------------------------------------------------
#  ESTE ARQUIVO TRATA OS DADOS DA "raw_vendas" E CARREGA A CAMADA TRATADA
# -------------------------------------------------------------------------------

# Configurações:
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from conexao import engine_supermarket

TABELA_RAW = "raw_vendas"
TABELA_TRATADA = "vendas_tratadas"
CAMINHO_CSV_TRATADO = (
    Path(__file__).resolve().parent.parent / "data" / "processed" / "vendas_tratadas.csv"
)

# Traduzindo nome das colunas:
NOME_COLUNAS = {
    "invoice_id": "id_venda",
    "branch": "filial",
    "city": "cidade",
    "customer_type": "tipo_cliente",
    "gender": "genero",
    "product_line": "linha_produto",
    "unit_price": "preco_unitario",
    "quantity": "quantidade",
    "tax_5": "imposto",
    "total": "valor_total",
    "date": "data_venda",
    "time": "hora_venda",
    "payment": "forma_pagamento",
    "cogs": "custo_mercadoria",
    "gross_margin_percentage": "margem_percentual",
    "gross_income": "receita_bruta",
    "rating": "avaliacao",
}


COLUNAS_TEXTO = [
    "id_venda", "filial", "cidade", "tipo_cliente",
    "genero", "linha_produto", "forma_pagamento",
]
COLUNAS_DECIMAIS = [
    "preco_unitario", "imposto", "valor_total",
    "custo_mercadoria", "margem_percentual", "receita_bruta", "avaliacao",
]


# Lê a camada raw:
def ler_raw():
    return pd.read_sql(f"SELECT * FROM {TABELA_RAW}", engine_supermarket)

# Descarta o id_raw (controle interno) e renomeia para o padrão da Tratada:
def renomear_colunas(df):
    df = df.drop(columns=["id_raw"])
    return df.rename(columns=NOME_COLUNAS)

# Remove espaços extras das colunas de texto:
def padronizar_textos(df):
    for coluna in COLUNAS_TEXTO:
        df[coluna] = df[coluna].str.strip()
    return df


# Converte texto para número, data e hora:
def converter_tipos(df):
    for coluna in COLUNAS_DECIMAIS:
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce").astype("Int64")
    df["data_venda"] = pd.to_datetime(
        df["data_venda"], format="%m/%d/%Y", errors="coerce"
    ).dt.date
    df["hora_venda"] = pd.to_datetime(
        df["hora_venda"], format="%I:%M:%S %p", errors="coerce"
    ).dt.time
    return df

# Cria colunas derivadas:
def criar_colunas_derivadas(df):
    datas = pd.to_datetime(df["data_venda"])
    df["dia_semana"] = datas.dt.day_name(locale="pt_BR").str.capitalize()
    df["nome_mes"] = datas.dt.month_name(locale="pt_BR").str.capitalize()
    return df

# Validação de tratamento de nulos e duplicados antes de gravar a tabela
def validar(df):
    nulos = df.isnull().sum().sum()
    duplicados = df["id_venda"].duplicated().sum()
    print(f"Nulos após conversão: {nulos} | id_venda duplicado: {duplicados}")
    return df.drop_duplicates(subset="id_venda")

# Grava a base tratada no PostgreSQL e em data/processed:
def carregar_tratada(df):
    with engine_supermarket.begin() as conexao:
        conexao.execute(text(f"TRUNCATE TABLE {TABELA_TRATADA}"))

    df.to_sql(TABELA_TRATADA, engine_supermarket, if_exists="append", index=False)
    df.to_csv(CAMINHO_CSV_TRATADO, index=False)


def main():
    df_raw = ler_raw()
    df_tratado = df_raw.copy()

    df_tratado = renomear_colunas(df_tratado)
    df_tratado = padronizar_textos(df_tratado)
    df_tratado = converter_tipos(df_tratado)
    df_tratado = criar_colunas_derivadas(df_tratado)

    carregar_tratada(df_tratado)

if __name__ == "__main__":
    main()
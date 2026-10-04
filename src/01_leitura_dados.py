# -------------------------------------------------------------------------------
#  ESTE ARQUIVO LÊ OS DADOS DA TABELA "raw_vendas" E FAZ A INSPEÇÃO ESTRUTURAL
# -------------------------------------------------------------------------------

# Configurações:
import pandas as pd

from conexao import engine_supermarket

COLUNAS_CATEGORIAS = [
    "branch", "city", "customer_type", "gender", "product_line", "payment",
]

# Leitura da tabela:
def ler_dados():
    return pd.read_sql("SELECT * FROM raw_vendas", engine_supermarket)


def inspecionar(df):
    print("Primeiras linhas")
    print(df.head())

    print("\n Dimensões")
    print(df.shape)

    print("\n Informações gerais")
    df.info()

    print("\n Valores nulos por coluna")
    print(df.isnull().sum())

    print("\n Linhas duplicadas")
    print(df.duplicated().sum())

    print("\n Duplicidade na identificação")
    print(df["invoice_id"].duplicated().sum())

    print("\n Valores únicos das colunas que possuem categoria")
    for coluna in COLUNAS_CATEGORIAS:
        print(f"\n{coluna}: {df[coluna].nunique()} valores")
        print(df[coluna].unique())


def main():
    df_raw = ler_dados()
    inspecionar(df_raw)


if __name__ == "__main__":
    main()
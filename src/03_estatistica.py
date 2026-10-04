# ---------------------------------------------------------------------------
# Análise estatística e perguntas de negócio
# ---------------------------------------------------------------------------

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------

raiz = Path(__file__).resolve().parent.parent

pasta_estatisticas = raiz / "resultados" / "estatisticas"
pasta_graficos = raiz / "resultados" / "graficos"

pasta_estatisticas.mkdir(parents=True, exist_ok=True)
pasta_graficos.mkdir(parents=True, exist_ok=True)


# Moeda e unidade de cada coluna usada nas estatísticas (coluna "unidade" do CSV)
MOEDA = "R$"

UNIDADES_COLUNAS = {
    "preco_unitario": MOEDA,
    "quantidade": "itens",
    "valor_total": MOEDA,
    "avaliacao": "nota"
}

# ---------------------------------------------------------------------------
# Leitura da base tratada
# ---------------------------------------------------------------------------

df = pd.read_csv(raiz / "data" / "processed" / "vendas_tratadas.csv")
df["data_venda"] = pd.to_datetime(df["data_venda"])


# ---------------------------------------------------------------------------
# Funções auxiliares
# ---------------------------------------------------------------------------

# Formata valores monetários no padrão brasileiro
def formatar_valor(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Salva o gráfico atual na pasta de gráficos
def salvar_grafico(nome):
    plt.tight_layout()
    plt.savefig(pasta_graficos / f"{nome}.png", dpi=150)
    plt.close()


# ---------------------------------------------------------------------------
# Estatísticas descritivas
# ---------------------------------------------------------------------------

# Estatísticas de faturamento por mês
ordem_meses = ["Janeiro", "Fevereiro", "Março"]

descricao_mes = (
    df.groupby("nome_mes")["valor_total"]
    .describe()
    .round(2)
    .reindex(ordem_meses)
)

print("\n Estatísticas de Faturamento por Mês")
print(descricao_mes)

# Estatísticas gerais das colunas importantes
colunas_analise = ["preco_unitario", "quantidade", "valor_total", "avaliacao"]

descricao = df[colunas_analise].describe().round(2)

print("\n Estatísticas Gerais de Colunas Importantes")
print(descricao)

# ---------------------------------------------------------------------------
# Perfil do cliente
# ---------------------------------------------------------------------------

perfil = (
    df.groupby(["tipo_cliente", "genero"])
    .agg(
        qtd_vendas=("id_venda", "count"),
        faturamento=("valor_total", "sum")
    )
    .sort_values("faturamento", ascending=False)
    .round(2)
)

print("\n Perfil do cliente ")
print(perfil)
print("Perfil que mais compra:", perfil.index[0])


# ---------------------------------------------------------------------------
# FATURAMENTO
# ---------------------------------------------------------------------------

print("\n Faturamento")


# Faturamento por filial
fat_filial = (
    df.groupby("filial")["valor_total"]
    .sum()
    .sort_values(ascending=False)
)

print(
    "Filial com maior faturamento:",
    fat_filial.idxmax(),
    formatar_valor(fat_filial.max())
)


# Faturamento por filial e tipo de cliente
fat_filial_tipo = (
    df.pivot_table(
        index="filial",
        columns="tipo_cliente",
        values="valor_total",
        aggfunc="sum"
    )
    .round(2)
)

print("\n Faturamento por filial e tipo de cliente:")
print(fat_filial_tipo)


fat_filial_tipo.plot(
    kind="bar",
    color=["tab:blue", "tab:green"],
    figsize=(8, 5)
)

plt.title("Faturamento por filial e tipo de cliente")
plt.xlabel("Filial")
plt.ylabel("Faturamento")
plt.xticks(rotation=0)
plt.legend(title="Tipo de cliente")

salvar_grafico("faturamento_filial_tipo_cliente")


# Participação das filiais no faturamento
participacao = fat_filial / fat_filial.sum() * 100

plt.figure(figsize=(6, 6))

plt.pie(
    fat_filial,
    labels=fat_filial.index,
    autopct=lambda p: f"{p:.2f}%".replace(".", ","),
    colors=["tab:blue", "tab:green", "tab:orange"],
    startangle=90
)

plt.title("Participação de cada filial no faturamento")

salvar_grafico("participacao_filial_faturamento")


# Faturamento por linha de produto
fat_linha = (
    df.groupby("linha_produto")["valor_total"]
    .sum()
    .sort_values(ascending=False)
)

print(
    "Linha com maior faturamento:",
    fat_linha.idxmax(),
    formatar_valor(fat_linha.max())
)


fig, ax = plt.subplots(figsize=(10, 6))

barras = ax.bar(
    fat_linha.index,
    fat_linha.values,
    color="tab:blue"
)

ax.bar_label(
    barras,
    labels=[formatar_valor(v) for v in fat_linha.values]
)

ax.set_title("Faturamento por linha de produto")
ax.set_xlabel("Linha de produto")
ax.set_ylabel("Faturamento")

plt.xticks(rotation=45, ha="right")

salvar_grafico("faturamento_por_linha")


# ---------------------------------------------------------------------------
# VENDAS
# ---------------------------------------------------------------------------

print("\n Vendas")


# Quantidade de vendas por filial
qtd_filial = df["filial"].value_counts()

print(
    "Filial com mais vendas:",
    qtd_filial.idxmax(),
    "-",
    qtd_filial.max(),
    "vendas"
)


qtd_filial.plot(
    kind="bar",
    color=["tab:blue", "tab:green", "tab:orange"],
    figsize=(8, 5)
)

plt.title("Quantidade de vendas por filial")
plt.xlabel("Filial")
plt.ylabel("Número de vendas")
plt.xticks(rotation=0)

salvar_grafico("vendas_por_filial")


# Maior venda
maior_venda = df.loc[df["valor_total"].idxmax()]

print("\n Maior venda registrada:", formatar_valor(maior_venda["valor_total"]))
print("ID da venda:", maior_venda["id_venda"])
print("Filial:", maior_venda["filial"])
print("Linha de produto:", maior_venda["linha_produto"])
print("Data:", maior_venda["data_venda"].date())


# Valor médio
valor_medio = df["valor_total"].mean()

print("Valor médio das vendas:", formatar_valor(valor_medio))


# Formas de pagamento
pagamento = df["forma_pagamento"].value_counts()

print(
    "Forma de pagamento mais utilizada:",
    pagamento.idxmax(),
    "-",
    pagamento.max(),
    "vendas"
)


pagamento.plot(
    kind="bar",
    color=["tab:blue", "tab:green", "tab:orange"],
    figsize=(8, 5)
)

plt.title("Formas de pagamento mais utilizadas")
plt.xlabel("Forma de pagamento")
plt.ylabel("Número de vendas")
plt.xticks(rotation=0)

salvar_grafico("formas_pagamento")


# Vendas por dia da semana
dias = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}

vendas_dia = (
    df["data_venda"]
    .dt.dayofweek
    .map(dias)
    .value_counts()
)

print(
    "Dia da semana com mais vendas:",
    vendas_dia.idxmax(),
    "-",
    vendas_dia.max(),
    "vendas"
)


# ---------------------------------------------------------------------------
# DESEMPENHO
# ---------------------------------------------------------------------------

print("\n Desempenho")


# Avaliação média por linha de produto
aval_linha = (
    df.groupby("linha_produto")["avaliacao"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print(aval_linha)

print(
    "Linha com melhor avaliação média:",
    aval_linha.idxmax(),
    "-",
    aval_linha.max()
)


# Avaliação média por tipo de cliente
aval_tipo = (
    df.groupby("tipo_cliente")["avaliacao"]
    .mean()
    .round(2)
    .sort_values(ascending=False)
)

print("\n Avaliação média por tipo de cliente:")
print(aval_tipo)


# ---------------------------------------------------------------------------
# CONSOLIDAÇÃO DAS MÉTRICAS
# ---------------------------------------------------------------------------

linhas = []

# Adiciona uma métrica à tabela consolidada
def adicionar(secao, metrica, dimensao, categoria, valor, unidade, subcategoria=""):
    linhas.append({
        "secao": secao,
        "metrica": metrica,
        "dimensao": dimensao,
        "categoria": categoria,
        "subcategoria": subcategoria,
        "valor": valor,
        "unidade": unidade
    })


# A contagem (count) é em vendas; as demais estatísticas usam a unidade da coluna
def unidade_estatistica(estatistica, unidade_coluna):
    return "vendas" if estatistica == "count" else unidade_coluna


# Estatísticas descritivas gerais
for coluna in descricao:
    for estatistica, valor in descricao[coluna].items():
        adicionar(
            "Estatísticas descritivas",
            estatistica,
            "coluna",
            coluna,
            valor,
            unidade_estatistica(estatistica, UNIDADES_COLUNAS[coluna])
        )

# Estatísticas descritivas do faturamento por mês
for mes, linha in descricao_mes.iterrows():
    for estatistica, valor in linha.items():
        adicionar(
            "Estatísticas descritivas",
            estatistica,
            "nome_mes",
            mes,
            valor,
            unidade_estatistica(estatistica, MOEDA),
            subcategoria="valor_total"
        )

# Perfil do cliente
for (tipo, genero), linha in perfil.iterrows():
    adicionar(
        "Perfil do cliente",
        "qtd_vendas",
        "tipo_cliente / genero",
        tipo,
        linha["qtd_vendas"],
        "vendas",
        subcategoria=genero
    )

    adicionar(
        "Perfil do cliente",
        "faturamento",
        "tipo_cliente / genero",
        tipo,
        linha["faturamento"],
        MOEDA,
        subcategoria=genero
    )


# Faturamento por filial
for filial, valor in fat_filial.items():
    adicionar(
        "Faturamento",
        "faturamento",
        "filial",
        filial,
        valor,
        MOEDA
    )

    adicionar(
        "Faturamento",
        "participacao_percentual",
        "filial",
        filial,
        participacao[filial],
        "%"
    )


# Faturamento por filial e tipo de cliente
for filial, linha in fat_filial_tipo.iterrows():
    for tipo, valor in linha.items():
        adicionar(
            "Faturamento",
            "faturamento",
            "filial / tipo_cliente",
            filial,
            valor,
            MOEDA,
            subcategoria=tipo
        )


# Faturamento por linha de produto
for produto, valor in fat_linha.items():
    adicionar(
        "Faturamento",
        "faturamento",
        "linha_produto",
        produto,
        valor,
        MOEDA
    )


# Vendas por filial
for filial, valor in qtd_filial.items():
    adicionar(
        "Vendas",
        "qtd_vendas",
        "filial",
        filial,
        valor,
        "vendas"
    )


# Maior venda: uma linha para cada atributo da venda, todas com o valor total dela
adicionar(
    "Vendas",
    "maior_venda",
    "id_venda",
    maior_venda["id_venda"],
    maior_venda["valor_total"],
    MOEDA
)

adicionar(
    "Vendas",
    "maior_venda",
    "filial",
    maior_venda["filial"],
    maior_venda["valor_total"],
    MOEDA
)

adicionar(
    "Vendas",
    "maior_venda",
    "linha_produto",
    maior_venda["linha_produto"],
    maior_venda["valor_total"],
    MOEDA
)

adicionar(
    "Vendas",
    "maior_venda",
    "data_venda",
    str(maior_venda["data_venda"].date()),
    maior_venda["valor_total"],
    MOEDA
)


# Valor médio
adicionar(
    "Vendas",
    "valor_medio",
    "geral",
    "todas",
    valor_medio,
    MOEDA
)


# Formas de pagamento
for forma, valor in pagamento.items():
    adicionar(
        "Vendas",
        "qtd_vendas",
        "forma_pagamento",
        forma,
        valor,
        "vendas"
    )


# Vendas por dia da semana
for dia, valor in vendas_dia.items():
    adicionar(
        "Vendas",
        "qtd_vendas",
        "dia_semana",
        dia,
        valor,
        "vendas"
    )


# Avaliação por linha de produto
for produto, valor in aval_linha.items():
    adicionar(
        "Desempenho",
        "avaliacao_media",
        "linha_produto",
        produto,
        valor,
        "nota"
    )


# Avaliação por tipo de cliente
for tipo, valor in aval_tipo.items():
    adicionar(
        "Desempenho",
        "avaliacao_media",
        "tipo_cliente",
        tipo,
        valor,
        "nota"
    )

# ---------------------------------------------------------------------------
# Exportação do único CSV de métricas
# ---------------------------------------------------------------------------

# Contagens ficam sem casas decimais (340) e as demais com 2 casas (330.37)
def limpar_numero(valor):
    valor = round(float(valor), 2)
    return int(valor) if valor.is_integer() else valor


metricas = pd.DataFrame(linhas)

metricas["valor"] = pd.Series(
    [limpar_numero(v) for v in metricas["valor"]],
    dtype=object
)

arquivo_saida = pasta_estatisticas / "metricas_analise.csv"

metricas.to_csv(
    arquivo_saida,
    index=False,
    encoding="utf-8-sig"
)

print("\n Análise concluída")
print(f"Métricas salvas em: {arquivo_saida}")
print(f"Total de métricas: {len(metricas)}")
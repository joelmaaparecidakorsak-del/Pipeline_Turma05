from pathlib import Path
import pandas as pd


# ==============================
# CONFIGURAÇÃO
# ==============================

SILVER_DIR = Path("silver")
GOLD_DIR = Path("gold")

GOLD_DIR.mkdir(exist_ok=True)


# ==============================
# LEITURA DA SILVER
# ==============================

viagem = pd.read_csv(
    SILVER_DIR / "viagem.csv",
    sep=";",
    encoding="utf-8-sig"
)

trecho = pd.read_csv(
    SILVER_DIR / "trecho.csv",
    sep=";",
    encoding="utf-8-sig"
)


# ==============================
# PADRONIZAÇÃO DAS COLUNAS-CHAVE
# ==============================

COLUNA_ID = "Identificador do processo de viagem"


# ==============================
# QUANTIDADE DE TRECHOS POR VIAGEM
# ==============================

qtd_trechos = (
    trecho
    .groupby(COLUNA_ID)
    .size()
    .rename("Quantidade de trechos")
)


# ==============================
# JUNÇÃO VIAGEM + QUANTIDADE DE TRECHOS
# ==============================

gold = viagem.merge(
    qtd_trechos,
    how="left",
    left_on=COLUNA_ID,
    right_index=True
)


# ==============================
# VIAGENS SEM TRECHO
# ==============================

gold["Quantidade de trechos"] = (
    gold["Quantidade de trechos"]
    .fillna(0)
    .astype("int64")
)

gold["Possui trecho"] = (
    gold["Quantidade de trechos"] > 0
)


# ==============================
# CONVERSÃO DOS VALORES
# ==============================

colunas_valores = [
    "Valor diárias",
    "Valor passagens",
    "Valor devolução",
    "Valor outros gastos"
]

for coluna in colunas_valores:
    gold[coluna] = pd.to_numeric(
        gold[coluna],
        errors="coerce"
    ).fillna(0)


# ==============================
# GASTO TOTAL
# ==============================

gold["Gasto total"] = (
    gold["Valor diárias"]
    + gold["Valor passagens"]
    + gold["Valor devolução"]
    + gold["Valor outros gastos"]
)


# ==============================
# SALVAR GOLD
# ==============================

arquivo_saida = GOLD_DIR / "viagens_resumo.csv"

gold.to_csv(
    arquivo_saida,
    sep=";",
    encoding="utf-8-sig",
    index=False
)


# ==============================
# VALIDAÇÕES
# ==============================

print("\n==============================")
print("GOLD - VIAGENS RESUMO")
print("==============================")

print("Linhas:", len(gold))
print("Colunas:", len(gold.columns))

print("\nQuantidade de viagens com trecho:")
print(gold["Possui trecho"].value_counts())

print("\nDistribuição da quantidade de trechos:")
print(gold["Quantidade de trechos"].describe())

print("\nGasto total:")
print(gold["Gasto total"].describe())

print("\nArquivo gerado:")
print(arquivo_saida)

# ==============================
# GOLD 2 - GASTOS POR ÓRGÃO
# ==============================

gold_orgao = (
    gold
    .groupby("Nome do órgão superior", dropna=False)
    .agg(
        quantidade_viagens=(
            "Identificador do processo de viagem",
            "count"
        ),
        viagens_com_trecho=(
            "Possui trecho",
            "sum"
        ),
        quantidade_trechos=(
            "Quantidade de trechos",
            "sum"
        ),
        valor_diarias=(
            "Valor diárias",
            "sum"
        ),
        valor_passagens=(
            "Valor passagens",
            "sum"
        ),
        valor_devolucao=(
            "Valor devolução",
            "sum"
        ),
        valor_outros_gastos=(
            "Valor outros gastos",
            "sum"
        ),
        gasto_total=(
            "Gasto total",
            "sum"
        )
    )
    .reset_index()
)


# ==============================
# VIAGENS SEM TRECHO
# ==============================

gold_orgao["viagens_sem_trecho"] = (
    gold_orgao["quantidade_viagens"]
    - gold_orgao["viagens_com_trecho"]
)


# ==============================
# PERCENTUAL SEM TRECHO
# ==============================

gold_orgao["percentual_sem_trecho"] = (
    gold_orgao["viagens_sem_trecho"]
    / gold_orgao["quantidade_viagens"]
    * 100
)


# ==============================
# ORDENAÇÃO
# ==============================

gold_orgao = gold_orgao.sort_values(
    "gasto_total",
    ascending=False
)


# ==============================
# SALVAR
# ==============================

arquivo_orgao = GOLD_DIR / "gastos_por_orgao.csv"

gold_orgao.to_csv(
    arquivo_orgao,
    sep=";",
    encoding="utf-8-sig",
    index=False
)


# ==============================
# VALIDAÇÃO
# ==============================

print("\n==============================")
print("GOLD - GASTOS POR ÓRGÃO")
print("==============================")

print("Quantidade de órgãos:", len(gold_orgao))

print("\nPrimeiros 10 órgãos por gasto total:")

print(
    gold_orgao[
        [
            "Nome do órgão superior",
            "quantidade_viagens",
            "quantidade_trechos",
            "gasto_total"
        ]
    ].head(10).to_string(index=False)
)

print("\nArquivo gerado:")
print(arquivo_orgao)

# ==============================
# GOLD 3 - GASTOS POR MÊS
# ==============================

# Converter data de início
gold["Período - Data de início"] = pd.to_datetime(
    gold["Período - Data de início"],
    errors="coerce"
)


# ==============================
# CRIAR ANO-MÊS
# ==============================

gold["Ano-Mês"] = (
    gold["Período - Data de início"]
    .dt.to_period("M")
    .astype("string")
)


# ==============================
# AGRUPAMENTO MENSAL
# ==============================

gold_mes = (
    gold
    .groupby("Ano-Mês", dropna=False)
    .agg(
        quantidade_viagens=(
            "Identificador do processo de viagem",
            "count"
        ),
        viagens_com_trecho=(
            "Possui trecho",
            "sum"
        ),
        quantidade_trechos=(
            "Quantidade de trechos",
            "sum"
        ),
        valor_diarias=(
            "Valor diárias",
            "sum"
        ),
        valor_passagens=(
            "Valor passagens",
            "sum"
        ),
        valor_devolucao=(
            "Valor devolução",
            "sum"
        ),
        valor_outros_gastos=(
            "Valor outros gastos",
            "sum"
        ),
        gasto_total=(
            "Gasto total",
            "sum"
        )
    )
    .reset_index()
)


# ==============================
# VIAGENS SEM TRECHO
# ==============================

gold_mes["viagens_sem_trecho"] = (
    gold_mes["quantidade_viagens"]
    - gold_mes["viagens_com_trecho"]
)


# ==============================
# PERCENTUAL SEM TRECHO
# ==============================

gold_mes["percentual_sem_trecho"] = (
    gold_mes["viagens_sem_trecho"]
    / gold_mes["quantidade_viagens"]
    * 100
)


# ==============================
# ORDENAÇÃO
# ==============================

gold_mes = gold_mes.sort_values("Ano-Mês")


# ==============================
# SALVAR
# ==============================

arquivo_mes = GOLD_DIR / "gastos_por_mes.csv"

gold_mes.to_csv(
    arquivo_mes,
    sep=";",
    encoding="utf-8-sig",
    index=False
)


# ==============================
# VALIDAÇÃO
# ==============================

print("\n==============================")
print("GOLD - GASTOS POR MÊS")
print("==============================")

print("Quantidade de períodos:", len(gold_mes))

print("\nResumo mensal:")

print(
    gold_mes[
        [
            "Ano-Mês",
            "quantidade_viagens",
            "quantidade_trechos",
            "gasto_total"
        ]
    ].to_string(index=False)
)

print("\nArquivo gerado:")
print(arquivo_mes)

# ==============================
# GOLD 4 - DESTINOS
# ==============================

gold_destinos = (
    trecho
    .groupby(
        [
            "Destino - País",
            "Destino - UF",
            "Destino - Cidade"
        ],
        dropna=False
    )
    .agg(
        quantidade_trechos=(
            "Identificador do processo de viagem",
            "count"
        ),
        quantidade_viagens=(
            "Identificador do processo de viagem",
            "nunique"
        )
    )
    .reset_index()
)


# ==============================
# ORDENAÇÃO
# ==============================

gold_destinos = gold_destinos.sort_values(
    "quantidade_trechos",
    ascending=False
)


# ==============================
# SALVAR
# ==============================

arquivo_destinos = GOLD_DIR / "destinos.csv"

gold_destinos.to_csv(
    arquivo_destinos,
    sep=";",
    encoding="utf-8-sig",
    index=False
)


# ==============================
# VALIDAÇÃO
# ==============================

print("\n==============================")
print("GOLD - DESTINOS")
print("==============================")

print(
    "Quantidade de destinos:",
    len(gold_destinos)
)

print("\n10 principais destinos por quantidade de trechos:")

print(
    gold_destinos[
        [
            "Destino - País",
            "Destino - UF",
            "Destino - Cidade",
            "quantidade_trechos",
            "quantidade_viagens"
        ]
    ]
    .head(10)
    .to_string(index=False)
)

print("\nArquivo gerado:")
print(arquivo_destinos)
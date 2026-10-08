
from pathlib import Path
import pandas as pd

SILVER_DIR = Path("silver")
GOLD_DIR = Path("gold")

# Ler as bases
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

resumo = pd.read_csv(
    GOLD_DIR / "viagens_resumo.csv",
    sep=";",
    encoding="utf-8-sig"
)

orgao = pd.read_csv(
    GOLD_DIR / "gastos_por_orgao.csv",
    sep=";",
    encoding="utf-8-sig"
)

mes = pd.read_csv(
    GOLD_DIR / "gastos_por_mes.csv",
    sep=";",
    encoding="utf-8-sig"
)

destinos = pd.read_csv(
    GOLD_DIR / "destinos.csv",
    sep=";",
    encoding="utf-8-sig"
)

print("\n=== VALIDACAO GOLD ===")

# Quantidades de registros
print("\n1. Quantidade de registros")
print("Silver VIAGEM:", len(viagem))
print("Gold resumo:", len(resumo))
print("Silver TRECHO:", len(trecho))
print("Gold destinos:", len(destinos))

assert len(viagem) == len(resumo), (
    "ERRO: quantidade de viagens diferente"
)

# Quantidade de trechos
print("\n2. Total de trechos")
total_silver = len(trecho)
total_gold = resumo["Quantidade de trechos"].sum()

print("Silver:", total_silver)
print("Gold:", int(total_gold))

assert total_silver == total_gold, (
    "ERRO: total de trechos diferente"
)

# Viagens sem trecho
sem_trecho = (
    resumo["Quantidade de trechos"] == 0
).sum()

print("\n3. Viagens sem trecho:", int(sem_trecho))

# Totais de gastos
colunas_valores = [
    "Valor diárias",
    "Valor passagens",
    "Valor devolução",
    "Valor outros gastos",
    "Gasto total"
]

print("\n4. Comparação dos gastos")


print("\n4. Comparação dos gastos")

colunas_valores = [
    "Valor diárias",
    "Valor passagens",
    "Valor devolução",
    "Valor outros gastos"
]

for coluna in colunas_valores:
    silver_total = pd.to_numeric(
        viagem[coluna], errors="coerce"
    ).fillna(0).sum()

    gold_total = pd.to_numeric(
        resumo[coluna], errors="coerce"
    ).fillna(0).sum()

    diferenca = gold_total - silver_total

    print(
        f"{coluna}: "
        f"Silver={silver_total:.2f} | "
        f"Gold={gold_total:.2f} | "
        f"Diferença={diferenca:.2f}"
    )

# Validar o gasto total calculado na Gold
gasto_calculado = resumo[
    [
        "Valor diárias",
        "Valor passagens",
        "Valor devolução",
        "Valor outros gastos"
    ]
].sum(axis=1)

diferenca_gasto = (
    resumo["Gasto total"] - gasto_calculado
).abs().max()

print(
    "\nMaior diferença no cálculo do gasto total:",
    round(diferenca_gasto, 2)
)

assert diferenca_gasto < 0.01, (
    "ERRO: gasto total diferente da soma das parcelas"
)
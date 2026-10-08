from pathlib import Path
import pandas as pd


# ==============================
# CONFIGURAÇÃO
# ==============================

SILVER_DIR = Path("silver")
GOLD_DIR = Path("gold")


# ==============================
# LEITURA DA SILVER
# ==============================

viagem = pd.read_csv(
    SILVER_DIR / "viagem.csv",
    sep=";",
    encoding="latin1"
)

trecho = pd.read_csv(
    SILVER_DIR / "trecho.csv",
    sep=";",
    encoding="latin1"
)


# ==============================
# INFORMAÇÕES
# ==============================

print("\n==============================")
print("VIAGEM")
print("==============================")

print("Linhas:", len(viagem))
print("Colunas:", len(viagem.columns))

print("\nColunas da VIAGEM:")

for coluna in viagem.columns:
    print("-", coluna)


print("\n==============================")
print("TRECHO")
print("==============================")

print("Linhas:", len(trecho))
print("Colunas:", len(trecho.columns))

print("\nColunas do TRECHO:")

for coluna in trecho.columns:
    print("-", coluna)
import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")

ARQUIVOS = [
    "2025_Viagem.csv",
    "2025_Trecho.csv",
    "2025_Pagamento.csv",
    "2025_Passagem.csv",
]


def diagnosticar(arquivo):
    caminho = DATA_DIR / arquivo

    print("\n" + "=" * 70)
    print(f"ARQUIVO: {arquivo}")
    print("=" * 70)

    # Lê apenas uma pequena amostra
    df = pd.read_csv(caminho, nrows=5)

    print("\nCOLUNAS:")
    for coluna in df.columns:
        print(f" - {coluna}")

    print("\nTIPOS:")
    print(df.dtypes)

    print("\nPRIMEIRAS 5 LINHAS:")
    print(df.to_string(index=False))


def main():
    for arquivo in ARQUIVOS:
        diagnosticar(arquivo)


if __name__ == "__main__":
    main()
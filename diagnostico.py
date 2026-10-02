import pandas as pd
from pathlib import Path


DATA_DIR = Path("data")


def analisar_pagamento():
    caminho = DATA_DIR / "2025_Pagamento.csv"

    print("\n" + "=" * 70)
    print("ANÁLISE DE DUPLICIDADES - PAGAMENTO")
    print("=" * 70)

    df = pd.read_csv(
        caminho,
        sep=";",
        encoding="latin1"
    )

    duplicados = df[df.duplicated(keep=False)]

    print(f"\nTotal de registros: {len(df):,}")
    print(f"Registros envolvidos em duplicidades: {len(duplicados):,}")

    print("\nExemplos de duplicidades:")

    print(
        duplicados
        .sort_values([
            "Identificador do processo de viagem",
            "Número da Proposta (PCDP)"
        ])
        .head(20)
        .to_string(index=False)
    )


def analisar_passagem():
    caminho = DATA_DIR / "2025_Passagem.csv"

    print("\n" + "=" * 70)
    print("ANÁLISE DE DUPLICIDADES - PASSAGEM")
    print("=" * 70)

    df = pd.read_csv(
        caminho,
        sep=";",
        encoding="latin1"
    )

    duplicados = df[df.duplicated(keep=False)]

    print(f"\nTotal de registros: {len(df):,}")
    print(f"Registros envolvidos em duplicidades: {len(duplicados):,}")

    print("\nExemplos de duplicidades:")

    print(
        duplicados
        .sort_values([
            "Identificador do processo de viagem",
            "Número da Proposta (PCDP)"
        ])
        .head(20)
        .to_string(index=False)
    )


def main():
    analisar_pagamento()
    analisar_passagem()


if __name__ == "__main__":
    main()
import pandas as pd
from pathlib import Path


SILVER_DIR = Path("silver")


def main():

    print("=" * 60)
    print("ANÁLISE DAS VIAGENS SEM TRECHO")
    print("=" * 60)

   #CARREGAR DADOS

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

    # IDENTIFICAR VIAGENS COM TRECHO

    ids_trecho = set(
        trecho["Identificador do processo de viagem"]
    )

    viagens_sem_trecho = viagem[
        ~viagem["Identificador do processo de viagem"].isin(ids_trecho)
    ].copy()

    print(
        f"\nViagens sem trecho: "
        f"{len(viagens_sem_trecho):,}"
    )


    # SITUAÇÃO

    print("\n" + "=" * 60)
    print("SITUAÇÃO DAS VIAGENS SEM TRECHO")
    print("=" * 60)

    print(
        viagens_sem_trecho["Situação"]
        .value_counts(dropna=False)
        .head(20)
    )


    # VIAGEM URGENTE

    print("\n" + "=" * 60)
    print("VIAGEM URGENTE")
    print("=" * 60)

    print(
        viagens_sem_trecho["Viagem Urgente"]
        .value_counts(dropna=False)
    )


    # VALORES FINANCEIROS

    colunas_valor = [
        "Valor diárias",
        "Valor passagens",
        "Valor devolução",
        "Valor outros gastos"
    ]

    print("\n" + "=" * 60)
    print("VALORES FINANCEIROS")
    print("=" * 60)

    for coluna in colunas_valor:

        total = viagens_sem_trecho[coluna].sum()

        quantidade = (
            viagens_sem_trecho[coluna]
            .notna()
            .sum()
        )

        print(
            f"{coluna}: "
            f"total = R$ {total:,.2f} | "
            f"preenchidos = {quantidade:,}"
        )


    # DATAS

    print("\n" + "=" * 60)
    print("PERÍODO DAS VIAGENS")
    print("=" * 60)

    print(
        "Data inicial mínima:",
        viagens_sem_trecho["Período - Data de início"].min()
    )

    print(
        "Data inicial máxima:",
        viagens_sem_trecho["Período - Data de início"].max()
    )

    # ÓRGÃOS

    print("\n" + "=" * 60)
    print("ÓRGÃOS SUPERIORES")
    print("=" * 60)

    print(
        viagens_sem_trecho[
            "Nome do órgão superior"
        ]
        .value_counts()
        .head(20)
    )

    # RESULTADO

    print("\n" + "=" * 60)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 60)


if __name__ == "__main__":
    main()
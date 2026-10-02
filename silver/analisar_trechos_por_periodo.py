import pandas as pd
from pathlib import Path


SILVER_DIR = Path("silver")


def main():

    print("=" * 60)
    print("ANÁLISE TEMPORAL DOS TRECHOS")
    print("=" * 60)

    # CARREGAR DADOS

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

    # CONVERTER DATAS

    viagem["Período - Data de início"] = pd.to_datetime(
        viagem["Período - Data de início"],
        errors="coerce"
    )

    trecho["Origem - Data"] = pd.to_datetime(
        trecho["Origem - Data"],
        errors="coerce"
    )

    trecho["Destino - Data"] = pd.to_datetime(
        trecho["Destino - Data"],
        errors="coerce"
    )

    # TRECHOS POR MÊS

    print("\n" + "=" * 60)
    print("TRECHOS POR MÊS - DATA DE ORIGEM")
    print("=" * 60)

    trechos_mes = (
        trecho
        .dropna(subset=["Origem - Data"])
        .assign(
            AnoMes=lambda df:
                df["Origem - Data"].dt.to_period("M")
        )
        .groupby("AnoMes")
        .size()
    )

    print(trechos_mes.to_string())


    # VIAGENS POR MÊS

    print("\n" + "=" * 60)
    print("VIAGENS POR MÊS - DATA DE INÍCIO")
    print("=" * 60)

    viagens_mes = (
        viagem
        .dropna(subset=["Período - Data de início"])
        .assign(
            AnoMes=lambda df:
                df["Período - Data de início"].dt.to_period("M")
        )
        .groupby("AnoMes")
        .size()
    )

    print(viagens_mes.to_string())


    # TRECHOS POR ÓRGÃO

    print("\n" + "=" * 60)
    print("TRECHOS POR ÓRGÃO SUPERIOR")
    print("=" * 60)

    ids_trecho = set(
        trecho["Identificador do processo de viagem"]
    )

    viagens_com_trecho = viagem[
        viagem["Identificador do processo de viagem"].isin(ids_trecho)
    ]

    print(
        viagens_com_trecho[
            "Nome do órgão superior"
        ]
        .value_counts()
        .head(20)
        .to_string()
    )

    # DATA MÍNIMA E MÁXIMA DOS TRECHOS

    print("\n" + "=" * 60)
    print("PERÍODO DOS TRECHOS")
    print("=" * 60)

    print(
        "Origem mínima:",
        trecho["Origem - Data"].min()
    )

    print(
        "Origem máxima:",
        trecho["Origem - Data"].max()
    )

    print(
        "Destino mínimo:",
        trecho["Destino - Data"].min()
    )

    print(
        "Destino máximo:",
        trecho["Destino - Data"].max()
    )


    print("\n" + "=" * 60)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 60)


if __name__ == "__main__":
    main()
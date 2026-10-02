import pandas as pd
from pathlib import Path


SILVER_DIR = Path("silver")


def main():

    print("=" * 60)
    print("VALIDAÇÃO DO RELACIONAMENTO VIAGEM x TRECHO")
    print("=" * 60)

   
    # CARREGAR ARQUIVOS DA SILVER

    print("\nCarregando viagem...")

    viagem = pd.read_csv(
        SILVER_DIR / "viagem.csv",
        sep=";",
        encoding="utf-8-sig"
    )

    print(f"Registros de viagem: {len(viagem):,}")

    print("\nCarregando trecho...")

    trecho = pd.read_csv(
        SILVER_DIR / "trecho.csv",
        sep=";",
        encoding="utf-8-sig"
    )

    print(f"Registros de trecho: {len(trecho):,}")


   
    # IDENTIFICADORES

    ids_viagem = set(
        viagem["Identificador do processo de viagem"]
    )

    ids_trecho = set(
        trecho["Identificador do processo de viagem"]
    )


    # PROCESSOS

    print("\n" + "=" * 60)
    print("PROCESSOS")
    print("=" * 60)

    print(
        f"Processos únicos na VIAGEM: "
        f"{len(ids_viagem):,}"
    )

    print(
        f"Processos únicos no TRECHO: "
        f"{len(ids_trecho):,}"
    )

    # TRECHOS SEM VIAGEM CORRESPONDENTE

    ids_sem_viagem = ids_trecho - ids_viagem

    print(
        f"\nTrechos sem processo correspondente na VIAGEM: "
        f"{len(ids_sem_viagem):,}"
    )


    # VIAGENS SEM TRECHO

    ids_sem_trecho = ids_viagem - ids_trecho

    print(
        f"Viagens sem nenhum TRECHO: "
        f"{len(ids_sem_trecho):,}"
    )


    # QUANTIDADE DE TRECHOS POR VIAGEM

    trechos_por_viagem = (
        trecho
        .groupby("Identificador do processo de viagem")
        .size()
    )

    print("\n" + "=" * 60)
    print("TRECHOS POR VIAGEM")
    print("=" * 60)

    print(
        f"Quantidade média de trechos por viagem: "
        f"{trechos_por_viagem.mean():.2f}"
    )

    print(
        f"Maior quantidade de trechos em uma viagem: "
        f"{trechos_por_viagem.max()}"
    )

    print(
        f"Menor quantidade de trechos em uma viagem: "
        f"{trechos_por_viagem.min()}"
    )

    # DISTRIBUIÇÃO

    print("\nDistribuição da quantidade de trechos:")

    print(
        trechos_por_viagem
        .value_counts()
        .sort_index()
        .head(20)
    )


    # FINAL

    print("\n" + "=" * 60)
    print("VALIDAÇÃO CONCLUÍDA")
    print("=" * 60)


if __name__ == "__main__":
    main()

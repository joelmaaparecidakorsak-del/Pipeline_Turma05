import pandas as pd
from pathlib import Path


SILVER_DIR = Path("silver")


def main():

    print("=" * 60)
    print("VALIDAÇÃO DAS CHAVES: PROCESSO x PCDP")
    print("=" * 60)

    # CARREGAR

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

    # IDENTIFICADORES DE PROCESSO

    ids_viagem = set(
        viagem["Identificador do processo de viagem"]
    )

    ids_trecho = set(
        trecho["Identificador do processo de viagem"]
    )

    viagens_sem_trecho = viagem[
        ~viagem["Identificador do processo de viagem"].isin(ids_trecho)
    ].copy()

    # PCDPs

    pcdps_trecho = set(
        trecho["Número da Proposta (PCDP)"]
        .dropna()
        .astype(str)
        .str.strip()
    )

    viagens_sem_trecho["PCDP"] = (
        viagens_sem_trecho["Número da Proposta (PCDP)"]
        .astype(str)
        .str.strip()
    )

    # VERIFICAR PCDPs ENCONTRADAS NO TRECHO

    correspondencias_pcdp = viagens_sem_trecho[
        viagens_sem_trecho["PCDP"].isin(pcdps_trecho)
    ].copy()

    print("\n" + "=" * 60)
    print("RESULTADO")
    print("=" * 60)

    print(
        f"Viagens sem trecho pelo IDENTIFICADOR: "
        f"{len(viagens_sem_trecho):,}"
    )

    print(
        f"Essas viagens encontradas pelo PCDP: "
        f"{len(correspondencias_pcdp):,}"
    )

    print(
        f"Essas viagens NÃO encontradas nem pelo PCDP: "
        f"{len(viagens_sem_trecho) - len(correspondencias_pcdp):,}"
    )

    # EXEMPLOS

    if len(correspondencias_pcdp) > 0:

        print("\nExemplos de correspondências pelo PCDP:")

        print(
            correspondencias_pcdp[
                [
                    "Identificador do processo de viagem",
                    "Número da Proposta (PCDP)",
                    "Nome do órgão superior",
                    "Período - Data de início"
                ]
            ]
            .head(20)
            .to_string(index=False)
        )

    # DUPLICIDADE DE PCDP NO TRECHO

    print("\n" + "=" * 60)
    print("DUPLICIDADE DE PCDP NO TRECHO")
    print("=" * 60)

    duplicadas = (
        trecho["Número da Proposta (PCDP)"]
        .value_counts()
    )

    print(
        f"PCDPs únicas no TRECHO: "
        f"{duplicadas.size:,}"
    )

    print(
        f"PCDPs com mais de um trecho: "
        f"{(duplicadas > 1).sum():,}"
    )

    print("\n" + "=" * 60)
    print("VALIDAÇÃO CONCLUÍDA")
    print("=" * 60)


if __name__ == "__main__":
    main()
